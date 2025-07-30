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

from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable, Union

from snowflake.snowflake_data_validation.configuration.model.table_configuration import (
    TableConfiguration,
)
from snowflake.snowflake_data_validation.configuration.model.validation_configuration import (
    ValidationConfiguration,
)
from snowflake.snowflake_data_validation.extractor.metadata_extractor_base import (
    MetadataExtractorBase,
)
from snowflake.snowflake_data_validation.script_writer.script_writer_base import (
    ScriptWriterBase,
)
from snowflake.snowflake_data_validation.utils.base_output_handler import (
    OutputMessageLevel,
)
from snowflake.snowflake_data_validation.utils.constants import (
    METRICS_VALIDATION_KEY,
    ROW_VALIDATION_KEY,
    SCHEMA_VALIDATION_KEY,
)
from snowflake.snowflake_data_validation.utils.context import Context
from snowflake.snowflake_data_validation.utils.logging_utils import log
from snowflake.snowflake_data_validation.utils.model.table_column_metadata import (
    TableColumnMetadata,
)


LOGGER = logging.getLogger(__name__)


def validation_handler(
    failure_header: str,
    failure_message_template: str = "Error during {operation}: {error}",
):
    """Provide consistent error handling for validation methods.

    This decorator provides consistent error handling for validation methods by:
    1. Wrapping method execution in try/catch block
    2. Handling success/failure message reporting
    3. Returning appropriate boolean results
    4. Providing consistent error message formatting

    Args:
        failure_header: Header message to use when validation fails
        failure_message_template: Template for failure message. Can use {operation} and {error} placeholders.

    Returns:
        Decorated method that handles errors and messaging consistently

    """

    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, table_context: TableConfiguration) -> bool:
            try:
                result = method(self, table_context)
                return result

            except Exception as e:
                operation = method.__name__.replace("execute_", "").replace("_", " ")

                formatted_message = failure_message_template.format(
                    operation=operation, error=str(e)
                )

                self.context.output_handler.handle_message(
                    header=failure_header,
                    message=formatted_message,
                    level=OutputMessageLevel.FAILURE,
                )
                return False

        return wrapper

    return decorator


class BaseValidationExecutor(ABC):

    """Base class for all validation executors.

    Implements the Template Method Pattern for table validation workflows.
    Defines the common interface and shared functionality for different
    validation execution strategies (sync validation, async generation, etc.).

    Subclasses must implement:
    - Individual validation methods (execute_schema_validation, etc.)
    - Message generation methods (_get_*_validation_message)
    """

    @log
    def __init__(
        self,
        source_extractor: Union[MetadataExtractorBase, ScriptWriterBase],
        target_extractor: Union[MetadataExtractorBase, ScriptWriterBase],
        context: Context,
    ):
        """Initialize the base validation executor.

        Args:
            source_extractor: Extractor for source metadata
            target_extractor: Extractor for target metadata
            context: Validation context containing configuration and runtime info

        """
        LOGGER.debug("Initializing BaseValidationExecutor")
        self.source_extractor = source_extractor
        self.target_extractor = target_extractor
        self.context = context
        LOGGER.debug(
            "BaseValidationExecutor initialized with source and target extractors"
        )

    @log
    def execute_validation_levels(
        self,
        validation_config: ValidationConfiguration,
        table_context: TableConfiguration,
    ) -> None:
        """Execute validation for all configured validations of a single table.

        Template Method: Defines the validation workflow while allowing subclasses
        to customize validation messages through abstract message methods.

        Args:
            validation_config: Configuration specifying which validations to run
            table_context: Table configuration containing all necessary validation parameters

        """
        validations = validation_config.model_dump()
        LOGGER.info(
            "Executing validation levels for table: %s",
            table_context.fully_qualified_name,
        )

        if not validations:
            LOGGER.warning(
                "No validations configured for table: %s",
                table_context.fully_qualified_name,
            )
            self.context.output_handler.handle_message(
                header="No validations configured.",
                message="No validation configuration found for the object.",
                level=OutputMessageLevel.WARNING,
            )
            return

        # TODO: L0 Load table column metadata model
        # table_column_metadata_model = self._load_table_column_metadata_model(object_name=object_name)

        if validations[SCHEMA_VALIDATION_KEY]:
            LOGGER.info(
                "Starting schema validation for table: %s",
                table_context.fully_qualified_name,
            )
            self.context.output_handler.handle_message(
                header="Schema validation started.",
                message=self._get_schema_validation_message(table_context),
                level=OutputMessageLevel.INFO,
            )
            self.execute_schema_validation(table_context)

        if validations[METRICS_VALIDATION_KEY]:
            LOGGER.info(
                "Starting metrics validation for table: %s",
                table_context.fully_qualified_name,
            )
            self.context.output_handler.handle_message(
                header="Metrics validation started.",
                message=self._get_metrics_validation_message(table_context),
                level=OutputMessageLevel.INFO,
            )
            self.execute_metrics_validation(table_context)

        if validations[ROW_VALIDATION_KEY]:
            LOGGER.info(
                "Starting row validation for table: %s",
                table_context.fully_qualified_name,
            )
            self.context.output_handler.handle_message(
                header="Row validation started.",
                message=self._get_row_validation_message(table_context),
                level=OutputMessageLevel.INFO,
            )
            self.execute_row_validation(table_context)

        LOGGER.info(
            "Completed all validation levels for table: %s",
            table_context.fully_qualified_name,
        )

    @log
    def _load_table_column_metadata_model(
        self, object_name: str
    ) -> TableColumnMetadata:
        LOGGER.debug("Loading table column metadata model for: %s", object_name)
        table_column_metadata_df = self.source_extractor.extract_table_column_metadata(
            object_name, self.context
        )

        table_column_metadata_model = TableColumnMetadata(table_column_metadata_df)
        LOGGER.debug(
            "Successfully loaded table column metadata model for: %s", object_name
        )
        return table_column_metadata_model

    @abstractmethod
    def execute_schema_validation(
        self,
        table_context: TableConfiguration,
    ) -> bool:
        """Execute schema validation for a table.

        Args:
            table_context: Table configuration containing all necessary validation parameters

        Returns:
            bool: True if validation passes, False otherwise

        """
        pass

    @abstractmethod
    def execute_metrics_validation(
        self,
        table_context: TableConfiguration,
    ) -> bool:
        """Execute metrics validation for a table.

        Args:
            table_context: Table configuration containing all necessary validation parameters

        Returns:
            bool: True if validation passes, False otherwise

        """
        pass

    @abstractmethod
    def execute_row_validation(
        self,
        table_context: TableConfiguration,
    ) -> bool:
        """Execute row validation for a table.

        Args:
            table_context: Table configuration containing all necessary validation parameters

        Returns:
            bool: True if validation passes, False otherwise

        """
        pass

    @abstractmethod
    def _get_schema_validation_message(self, table_context: TableConfiguration) -> str:
        """Get operation-specific message for schema validation.

        Args:
            table_context: Table configuration containing all necessary validation parameters

        Returns:
            str: Operation-specific message for schema validation

        """
        pass

    @abstractmethod
    def _get_metrics_validation_message(self, table_context: TableConfiguration) -> str:
        """Get operation-specific message for metrics validation.

        Template Method Hook: Subclasses customize messaging for their operation type.

        Args:
            table_context: Table configuration containing all necessary validation parameters

        Returns:
            str: Operation-specific message for metrics validation

        """
        pass

    @abstractmethod
    def _get_row_validation_message(self, table_context: TableConfiguration) -> str:
        """Get operation-specific message for row validation.

        Template Method Hook: Subclasses customize messaging for their operation type.

        Args:
            table_context: Table configuration containing all necessary validation parameters

        Returns:
            str: Operation-specific message for row validation

        """
        pass
