# Copyright 2025 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import pandas as pd

from pandas.testing import assert_frame_equal

from snowflake.snowflake_data_validation.utils.base_output_handler import (
    OutputMessageLevel,
)
from snowflake.snowflake_data_validation.utils.constants import (
    COLUMN_DATATYPE,
    COLUMN_VALIDATED,
    NOT_EXIST_TARGET,
    TABLE_NAME_KEY,
    ValidationLevel,
)
from snowflake.snowflake_data_validation.utils.context import Context
from snowflake.snowflake_data_validation.utils.helpers import (
    is_numeric,
    normalize_dataframe,
)
from snowflake.snowflake_data_validation.utils.logging_utils import log
from snowflake.snowflake_data_validation.validation.validation_report_buffer import (
    ValidationReportBuffer,
)


LOGGER = logging.getLogger(__name__)

VALIDATION_REPORT_NAME = "data_validation_report.csv"


@log
def general_validation(
    target_df: pd.DataFrame, source_df: pd.DataFrame, context: Context
) -> tuple:
    """Validate the consistency between two DataFrames by comparing their columns and values.

    This function checks for the following:
    1. Columns that are only present in the target DataFrame but not in the source DataFrame.
    2. Columns that are only present in the source DataFrame but not in the target DataFrame.
    3. Columns that are common between the two DataFrames but have differing values.

    If discrepancies are found, messages are logged using the provided context's output handler.
    If no discrepancies are found, the function returns True.

    Args:
        target_df (pd.DataFrame): The target DataFrame to validate.
        source_df (pd.DataFrame): The source DataFrame to validate against.
        context (Context): The context object containing an output handler for logging messages.

    Returns:
        tuple: A tuple containing (differing_cols, result) where:
            - differing_cols is a list of column names with differences
            - result is a boolean indicating if the validation passed (True) or failed (False)

    """
    LOGGER.info("Starting general validation between target and source DataFrames")
    target_cols = set(target_df.columns)
    source_cols = set(source_df.columns)
    differing_cols = []

    LOGGER.debug("Target DataFrame columns: %s", target_cols)
    LOGGER.debug("Source DataFrame columns: %s", source_cols)

    try:
        assert_frame_equal(target_df, source_df, check_exact=True)
        LOGGER.info("DataFrames are identical - validation passed")
        return differing_cols, True
    except:  # noqa: E722
        LOGGER.debug("DataFrames differ - analyzing differences")
        cols_only_in_target = target_cols - source_cols
        cols_only_in_source = source_cols - target_cols
        common_cols = source_cols & target_cols

        if len(cols_only_in_target) > 0:
            LOGGER.warning("Columns only in target: %s", cols_only_in_target)
            context.output_handler.handle_message(
                header=f"Metric only in Snowflake table: {cols_only_in_target} will be ignored from validation.",
                message="",
                level=OutputMessageLevel.ERROR,
            )
        if len(cols_only_in_source) > 0:
            LOGGER.warning("Columns only in source: %s", cols_only_in_source)
            context.output_handler.handle_message(
                header=f"Metric only in source table: {cols_only_in_source} will be ignored from validation.",
                message="",
                level=OutputMessageLevel.ERROR,
            )
        for col in common_cols:
            if not target_df[col].equals(source_df[col]):
                differing_cols.append(col)

        if len(differing_cols) > 0:
            LOGGER.info("Columns with different values: %s", differing_cols)
            context.output_handler.handle_message(
                header=f"Columns with different values: {differing_cols}",
                message="",
                level=OutputMessageLevel.INFO,
            )

        # Return False if there are any differences, True otherwise
        validation_passed = len(differing_cols) == 0
        LOGGER.info("General validation completed - passed: %s", validation_passed)
        return differing_cols, validation_passed


@log
def validate_table_metadata(
    object_name: str, target_df: pd.DataFrame, source_df: pd.DataFrame, context: Context
) -> bool:
    """Validate the metadata of two tables by normalizing and comparing their dataframes.

    Args:
        object_name (str): The name of the object (e.g., table) being validated.
        target_df (pd.DataFrame): The dataframe representing the target table's metadata.
        source_df (pd.DataFrame): The dataframe representing the source table's metadata.
        context (Context): The execution context containing relevant configuration and runtime information.

    Returns:
        bool: True if the normalized dataframes are equal, False otherwise.

    """
    LOGGER.info("Starting table metadata validation for: %s", object_name)
    context.output_handler.handle_message(
        message=f"Running Schema Validation for {object_name}",
        level=OutputMessageLevel.INFO,
    )

    LOGGER.debug("Normalizing target and source DataFrames")
    normalized_target = normalize_dataframe(target_df)
    normalized_source = normalize_dataframe(source_df)

    differences_data = pd.DataFrame(
        columns=[
            "VALIDATION_TYPE",
            "TABLE",
            "COLUMN_VALIDATED",
            "EVALUATION_CRITERIA",
            "SOURCE_VALUE",
            "SNOWFLAKE_VALUE",
            "STATUS",
            "COMMENTS",
        ]
    )

    target_validated_set = set(normalized_target[COLUMN_VALIDATED].values)
    has_differences = False

    for _, source_row in normalized_source.iterrows():
        source_validated_value = source_row[COLUMN_VALIDATED]

        if source_validated_value not in target_validated_set:
            LOGGER.debug("Column %s not found in target table", source_validated_value)
            new_row = pd.DataFrame(
                {
                    "VALIDATION_TYPE": [ValidationLevel.SCHEMA_VALIDATION.value],
                    "TABLE": [object_name],
                    "COLUMN_VALIDATED": [source_validated_value],
                    "EVALUATION_CRITERIA": [COLUMN_VALIDATED],
                    "SOURCE_VALUE": [source_validated_value],
                    "SNOWFLAKE_VALUE": [NOT_EXIST_TARGET],
                    "STATUS": ["FAILURE"],
                    "COMMENTS": ["The column does not exist in the target table."],
                }
            )
            differences_data = pd.concat([differences_data, new_row], ignore_index=True)
            has_differences = True
        else:
            target_row = normalized_target[
                normalized_target[COLUMN_VALIDATED] == source_validated_value
            ]

            column_has_differences = False

            for column in normalized_source.columns:
                # Skip the columns that are not relevant to the validation
                if column == COLUMN_VALIDATED or column == TABLE_NAME_KEY:
                    continue

                source_value = source_row[column]
                target_value = target_row[column].values[0]

                # Skip if both values are NaN or identical
                if pd.isna(source_value) and pd.isna(target_value):
                    continue
                if source_value == target_value:
                    success_row = pd.DataFrame(
                        {
                            "VALIDATION_TYPE": [
                                ValidationLevel.SCHEMA_VALIDATION.value
                            ],
                            "TABLE": [object_name],
                            "COLUMN_VALIDATED": [source_validated_value],
                            "EVALUATION_CRITERIA": [column],
                            "SOURCE_VALUE": [source_value],
                            "SNOWFLAKE_VALUE": [target_value],
                            "STATUS": ["SUCCESS"],
                            "COMMENTS": [
                                f"Values match: source({source_value}), Snowflake({target_value})"
                            ],
                        }
                    )
                    differences_data = pd.concat(
                        [differences_data, success_row], ignore_index=True
                    )
                    continue

                has_differences = True
                column_has_differences = True

                if column == COLUMN_DATATYPE and context.datatypes_mappings:
                    mapped_value = context.datatypes_mappings.get(
                        source_value.upper(), []
                    )
                    if target_value.upper() != mapped_value:
                        LOGGER.debug(
                            "Datatype mismatch for column %s: source=%s, target=%s",
                            source_validated_value,
                            source_value,
                            target_value,
                        )
                        new_row = pd.DataFrame(
                            {
                                "VALIDATION_TYPE": [
                                    ValidationLevel.SCHEMA_VALIDATION.value
                                ],
                                "TABLE": [object_name],
                                "COLUMN_VALIDATED": [source_validated_value],
                                "EVALUATION_CRITERIA": [column],
                                "SOURCE_VALUE": [source_value],
                                "SNOWFLAKE_VALUE": [target_value],
                                "STATUS": ["FAILURE"],
                                "COMMENTS": [
                                    f"Values differ: source({source_value}), Snowflake({target_value})"
                                ],
                            }
                        )
                        if not new_row.empty:
                            differences_data = (
                                pd.concat(
                                    [differences_data, new_row], ignore_index=True
                                )
                                if not differences_data.empty
                                else new_row
                            )
                    else:
                        success_row = pd.DataFrame(
                            {
                                "VALIDATION_TYPE": [
                                    ValidationLevel.SCHEMA_VALIDATION.value
                                ],
                                "TABLE": [object_name],
                                "COLUMN_VALIDATED": [source_validated_value],
                                "EVALUATION_CRITERIA": [column],
                                "SOURCE_VALUE": [source_value],
                                "SNOWFLAKE_VALUE": [target_value],
                                "STATUS": ["SUCCESS"],
                                "COMMENTS": [
                                    (
                                        "Datatype mapping successful: "
                                        f"source({source_value}) maps to Snowflake({target_value})"
                                    )
                                ],
                            }
                        )
                        differences_data = pd.concat(
                            [differences_data, success_row], ignore_index=True
                        )
                        column_has_differences = False
                        has_differences = False
                else:
                    LOGGER.debug(
                        "Value mismatch for column %s in %s: source=%s, target=%s",
                        source_validated_value,
                        column,
                        source_value,
                        target_value,
                    )
                    new_row = pd.DataFrame(
                        {
                            "VALIDATION_TYPE": [
                                ValidationLevel.SCHEMA_VALIDATION.value
                            ],
                            "TABLE": [object_name],
                            "COLUMN_VALIDATED": [source_validated_value],
                            "EVALUATION_CRITERIA": [column],
                            "SOURCE_VALUE": [source_value],
                            "SNOWFLAKE_VALUE": [target_value],
                            "STATUS": ["FAILURE"],
                            "COMMENTS": [
                                f"Values differ: source({source_value}), Snowflake({target_value})"
                            ],
                        }
                    )
                    if not new_row.empty:
                        differences_data = (
                            pd.concat([differences_data, new_row], ignore_index=True)
                            if not differences_data.empty
                            else new_row
                        )

            # If the column exists in target but had no individual field differences, record overall success
            if not column_has_differences:
                success_row = pd.DataFrame(
                    {
                        "VALIDATION_TYPE": [ValidationLevel.SCHEMA_VALIDATION.value],
                        "TABLE": [object_name],
                        "COLUMN_VALIDATED": [source_validated_value],
                        "EVALUATION_CRITERIA": [COLUMN_VALIDATED],
                        "SOURCE_VALUE": [source_validated_value],
                        "SNOWFLAKE_VALUE": [source_validated_value],
                        "STATUS": ["SUCCESS"],
                        "COMMENTS": [
                            "Column exists in target table and all metadata matches."
                        ],
                    }
                )
                differences_data = pd.concat(
                    [differences_data, success_row], ignore_index=True
                )

    buffer = ValidationReportBuffer()
    buffer.add_data(differences_data)
    LOGGER.debug(
        "Added schema validation data for %s to buffer (queue size: %d)",
        object_name,
        buffer.get_queue_size(),
    )

    display_data = differences_data.drop(
        columns=["VALIDATION_TYPE", "TABLE"], errors="ignore"
    )

    context.output_handler.handle_message(
        header="Schema validation results:",
        dataframe=display_data,
        level=(
            OutputMessageLevel.WARNING if has_differences else OutputMessageLevel.INFO
        ),
    )

    return not has_differences


@log
def validate_column_metadata(
    object_name: str,
    target_df: pd.DataFrame,
    source_df: pd.DataFrame,
    context: Context,
    tolerance: float = 0.001,
) -> bool:
    """Validate that the column metadata of the target DataFrame matches the source DataFrame.

    This method normalizes both the target and source DataFrames and then compares their
    column metadata cell by cell to ensure they are equivalent within a given tolerance.

    Args:
        object_name (str): The name of the object (e.g., table) being validated.
        target_df (pd.DataFrame): The target DataFrame whose column metadata is to be validated.
        source_df (pd.DataFrame): The source DataFrame to compare against.
        context (Context): The execution context containing relevant configuration and runtime information.
        tolerance (float, optional): The tolerance level for numerical differences. Defaults to 0.001.

    Returns:
        bool: True if the column metadata of both DataFrames are equal within the tolerance, False otherwise.

    """
    LOGGER.info(
        "Starting column metadata validation for: %s with tolerance: %f",
        object_name,
        tolerance,
    )
    context.output_handler.handle_message(
        message=f"Running Metrics Validation for {object_name}",
        level=OutputMessageLevel.INFO,
    )

    normalized_target = normalize_dataframe(target_df)
    normalized_source = normalize_dataframe(source_df)

    differences_data = pd.DataFrame(
        columns=[
            "VALIDATION_TYPE",
            "TABLE",
            "COLUMN_VALIDATED",
            "EVALUATION_CRITERIA",
            "SOURCE_VALUE",
            "SNOWFLAKE_VALUE",
            "STATUS",
            "COMMENTS",
        ]
    )
    target_validated_set = set(normalized_target[COLUMN_VALIDATED].values)

    has_differences = False

    for _, source_row in normalized_source.iterrows():
        column_name = source_row[COLUMN_VALIDATED]
        source_validated_value = source_row[COLUMN_VALIDATED]

        if source_validated_value not in target_validated_set:
            new_row = pd.DataFrame(
                {
                    "VALIDATION_TYPE": [ValidationLevel.METRICS_VALIDATION.value],
                    "TABLE": [object_name],
                    "COLUMN_VALIDATED": [source_validated_value],
                    "EVALUATION_CRITERIA": [COLUMN_VALIDATED],
                    "SOURCE_VALUE": [source_validated_value],
                    "SNOWFLAKE_VALUE": [NOT_EXIST_TARGET],
                    "STATUS": ["FAILURE"],
                    "COMMENTS": ["The column does not exist in the target table."],
                }
            )
            differences_data = pd.concat([differences_data, new_row], ignore_index=True)
            has_differences = True
        else:
            target_row = normalized_target[
                normalized_target[COLUMN_VALIDATED] == source_validated_value
            ]

            column_has_differences = False

            for col in normalized_source.columns:
                if col == COLUMN_VALIDATED or col == TABLE_NAME_KEY:
                    continue

                source_value = source_row[col]
                target_value = target_row[col].values[0]

                # Skip if both values are NaN or identical
                if pd.isna(source_value) and pd.isna(target_value):
                    # Record successful validation for NaN values
                    success_row = pd.DataFrame(
                        {
                            "VALIDATION_TYPE": [
                                ValidationLevel.METRICS_VALIDATION.value
                            ],
                            "TABLE": [object_name],
                            "COLUMN_VALIDATED": [column_name],
                            "EVALUATION_CRITERIA": [col],
                            "SOURCE_VALUE": ["NULL"],
                            "SNOWFLAKE_VALUE": ["NULL"],
                            "STATUS": ["SUCCESS"],
                            "COMMENTS": [
                                "Both values are NULL/NaN - validation passed"
                            ],
                        }
                    )
                    differences_data = pd.concat(
                        [differences_data, success_row], ignore_index=True
                    )
                    continue
                if source_value == target_value:
                    # Record successful validation for exact matches
                    success_row = pd.DataFrame(
                        {
                            "VALIDATION_TYPE": [
                                ValidationLevel.METRICS_VALIDATION.value
                            ],
                            "TABLE": [object_name],
                            "COLUMN_VALIDATED": [column_name],
                            "EVALUATION_CRITERIA": [col],
                            "SOURCE_VALUE": [str(source_value)],
                            "SNOWFLAKE_VALUE": [str(target_value)],
                            "STATUS": ["SUCCESS"],
                            "COMMENTS": [f"Values match exactly: {source_value}"],
                        }
                    )
                    differences_data = pd.concat(
                        [differences_data, success_row], ignore_index=True
                    )
                    continue

                # Check numeric values with tolerance
                if is_numeric(source_value) and is_numeric(target_value):
                    source_num = float(source_value)
                    target_num = float(target_value)
                    if abs(source_num - target_num) <= tolerance:
                        # Record successful validation within tolerance
                        success_row = pd.DataFrame(
                            {
                                "VALIDATION_TYPE": [
                                    ValidationLevel.METRICS_VALIDATION.value
                                ],
                                "TABLE": [object_name],
                                "COLUMN_VALIDATED": [column_name],
                                "EVALUATION_CRITERIA": [col],
                                "SOURCE_VALUE": [str(source_value)],
                                "SNOWFLAKE_VALUE": [str(target_value)],
                                "STATUS": ["SUCCESS"],
                                "COMMENTS": [
                                    (
                                        f"Values within tolerance ({tolerance}): "
                                        f"source({source_value}), target({target_value})"
                                    )
                                ],
                            }
                        )
                        differences_data = pd.concat(
                            [differences_data, success_row], ignore_index=True
                        )
                        continue
                    comment = (
                        f"Values differ beyond tolerance of {tolerance}: "
                        f"source({source_value}), target({target_value})"
                    )
                else:
                    comment = (
                        f"Values differ: source({source_value}), target({target_value})"
                    )

                column_has_differences = True
                has_differences = True
                new_row = pd.DataFrame(
                    {
                        "VALIDATION_TYPE": [ValidationLevel.METRICS_VALIDATION.value],
                        "TABLE": [object_name],
                        "COLUMN_VALIDATED": [column_name],
                        "EVALUATION_CRITERIA": [col],
                        "SOURCE_VALUE": [str(source_value)],
                        "SNOWFLAKE_VALUE": [str(target_value)],
                        "STATUS": ["FAILURE"],
                        "COMMENTS": [comment],
                    }
                )
                differences_data = pd.concat(
                    [differences_data, new_row], ignore_index=True
                )

            # If the column exists and had no differences, record overall column success
            if not column_has_differences:
                success_row = pd.DataFrame(
                    {
                        "VALIDATION_TYPE": [ValidationLevel.METRICS_VALIDATION.value],
                        "TABLE": [object_name],
                        "COLUMN_VALIDATED": [column_name],
                        "EVALUATION_CRITERIA": [COLUMN_VALIDATED],
                        "SOURCE_VALUE": [source_validated_value],
                        "SNOWFLAKE_VALUE": [source_validated_value],
                        "STATUS": ["SUCCESS"],
                        "COMMENTS": [
                            "Column exists in target table and all metrics match."
                        ],
                    }
                )
                differences_data = pd.concat(
                    [differences_data, success_row], ignore_index=True
                )

    # Add validation data to buffer instead of writing directly to file
    buffer = ValidationReportBuffer()
    buffer.add_data(differences_data)
    LOGGER.debug(
        "Added metrics validation data for %s to buffer (queue size: %d)",
        object_name,
        buffer.get_queue_size(),
    )

    display_data = differences_data.drop(
        columns=["VALIDATION_TYPE", "TABLE"], errors="ignore"
    )

    context.output_handler.handle_message(
        header="Metrics validation results:",
        dataframe=display_data,
        level=(
            OutputMessageLevel.WARNING if has_differences else OutputMessageLevel.INFO
        ),
    )

    return not has_differences


@log
def validate_non_numeric_difference(
    differences_data, object_name, column_name, metric, source_value, target_value
):
    """Validate non-numeric differences between source and target values for a specific column and metric.

    This function checks if there is a difference between the source and target values for a given column and metric.
    If a difference is found, it creates a new metadata row describing the discrepancy and appends it to the
    `differences_data` DataFrame.

    Args:
        differences_data (pd.DataFrame): A DataFrame containing metadata about differences identified during validation.
        object_name (str): The name of the object (e.g., table) being validated.
        column_name (str): The name of the column being validated.
        metric (str): The metric or validation rule being applied.
        source_value (Any): The value from the source dataset.
        target_value (Any): The value from the target dataset.

    Returns:
        pd.DataFrame: An updated DataFrame with the original differences and a new row if a difference was found.

    """
    LOGGER.debug(
        "Validating non-numeric difference for %s.%s.%s: source=%s, target=%s",
        object_name,
        column_name,
        metric,
        source_value,
        target_value,
    )
    new_row = pd.DataFrame(
        {
            "VALIDATION_TYPE": [ValidationLevel.METRICS_VALIDATION.value],
            "TABLE": [object_name],
            "COLUMN_VALIDATED": [column_name],
            "EVALUATION_CRITERIA": [metric],
            "SOURCE_VALUE": [source_value],
            "SNOWFLAKE_VALUE": [target_value],
            "STATUS": ["FAILURE"],
            "COMMENTS": [
                f"Values differ: source({source_value}), target({target_value})."
            ],
        }
    )
    if not new_row.empty:
        differences_data = (
            pd.concat([differences_data, new_row], ignore_index=True)
            if not differences_data.empty
            else new_row
        )

    return differences_data


@log
def validate_numeric_difference(
    tolerance: float,
    differences_data: pd.DataFrame,
    object_name: str,
    column_name: str,
    metric: str,
    source_value: any,
    target_value: any,
    context: Context,
):
    """Validate the numeric difference between source and target values against a specified tolerance.

    This function checks if the absolute difference between the source and target values exceeds the given tolerance.
    If the difference is greater than the tolerance, it creates a new metadata row describing the discrepancy and
    appends it to the `differences_data` DataFrame.

    Args:
        tolerance (float): The maximum allowable difference between the source and target values.
        differences_data (pd.DataFrame): A DataFrame containing metadata about detected differences.
        object_name (str): The name of the object (e.g., table) being validated.
        column_name (str): The name of the column being validated.
        metric (str): The metric or description associated with the validation.
        source_value (float or str): The source value to be compared.
        target_value (float or str): The target value to be compared.
        context (Context): The execution context containing relevant configuration and runtime information.

    Returns:
        tuple: A tuple containing:
            - differences_data (pd.DataFrame): The updated DataFrame with any new discrepancy metadata rows appended.
            - source_value (float): The source value converted to a float.
            - target_value (float): The target value converted to a float.

    Raises:
        ValueError: If the source or target values cannot be converted to floats.

    Notes:
        - If the `differences_data` DataFrame is empty, it initializes it with the new metadata row.

    """
    LOGGER.debug(
        "Validating numeric difference for %s.%s.%s with tolerance %f: source=%s, target=%s",
        object_name,
        column_name,
        metric,
        tolerance,
        source_value,
        target_value,
    )
    # WIP: This is a temporary solution to handle the case when the value is a string representation of a number.
    target_value = float(target_value)
    source_value = float(source_value)
    if abs(target_value - source_value) > tolerance:
        new_row = pd.DataFrame(
            {
                "VALIDATION_TYPE": [ValidationLevel.METRICS_VALIDATION.value],
                "TABLE": [object_name],
                "COLUMN_VALIDATED": [column_name],
                "EVALUATION_CRITERIA": [metric],
                "SOURCE_VALUE": [source_value],
                "SNOWFLAKE_VALUE": [target_value],
                "STATUS": ["FAILURE"],
                "COMMENTS": [
                    f"Values differ ({source_value} != {target_value}) beyond tolerance."
                ],
            }
        )
        if not new_row.empty:
            differences_data = (
                pd.concat([differences_data, new_row], ignore_index=True)
                if not differences_data.empty
                else new_row
            )
    else:
        context.output_handler.handle_message(
            header="Disregarding numeric difference.",
            message=(
                f"Source value: {source_value} and Target value: {target_value} "
                f"do not differ beyond tolerance. {tolerance}"
            ),
            level=OutputMessageLevel.WARNING,
        )
    return differences_data, source_value, target_value
