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

from snowflake.snowflake_data_validation.configuration.model.table_configuration import (
    TableConfiguration,
)
from snowflake.snowflake_data_validation.executer.base_validation_executor import (
    BaseValidationExecutor,
    validation_handler,
)
from snowflake.snowflake_data_validation.utils.base_output_handler import (
    OutputMessageLevel,
)
from snowflake.snowflake_data_validation.utils.logging_utils import log
from snowflake.snowflake_data_validation.validation import data_validator


LOGGER = logging.getLogger(__name__)


class SyncValidationExecutor(BaseValidationExecutor):

    """Executor for synchronous validation operations.

    This executor performs real-time validation by extracting metadata from both
    source and target systems and comparing them immediately. Used for run-validation
    and run-validation-ipc commands.
    """

    @validation_handler("Schema validation failed.")
    @log
    def execute_schema_validation(
        self,
        table_context: TableConfiguration,
    ) -> bool:
        """Execute schema validation by comparing table metadata.

        Args:
            table_context: Table configuration containing all necessary validation parameters

        Returns:
            bool: True if validation passes, False otherwise

        """
        LOGGER.info(
            "Starting schema validation for table: %s",
            table_context.fully_qualified_name,
        )

        extraction_message = (
            f"Extracting Schema metadata for: "
            f"{table_context.fully_qualified_name} on {{}}"
        )

        self.context.output_handler.handle_message(
            message=extraction_message.format(self.context.source_platform.value),
            level=OutputMessageLevel.INFO,
        )
        LOGGER.debug("Extracting source schema metadata")
        source_metadata = self.source_extractor.extract_schema_metadata(
            table_context,
            self.context,
        )

        self.context.output_handler.handle_message(
            message=extraction_message.format(self.context.target_platform.value),
            level=OutputMessageLevel.INFO,
        )
        LOGGER.debug("Extracting target schema metadata")
        target_metadata = self.target_extractor.extract_schema_metadata(
            table_context,
            self.context,
        )

        LOGGER.debug("Validating schema metadata")
        validation_result = data_validator.validate_table_metadata(
            object_name=table_context.fully_qualified_name,
            target_df=target_metadata,
            source_df=source_metadata,
            context=self.context,
        )
        validation_status = "passed" if validation_result else "failed"
        LOGGER.info(
            "Schema validation %s for table: %s",
            validation_status,
            table_context.fully_qualified_name,
        )
        self.context.output_handler.handle_message(
            header=f"Schema validation {validation_status}.",
            message="",
            level=OutputMessageLevel.SUCCESS
            if validation_result
            else OutputMessageLevel.FAILURE,
        )
        return validation_result

    @validation_handler("Metrics validation failed.")
    @log
    def execute_metrics_validation(
        self,
        table_context: TableConfiguration,
    ) -> bool:
        """Execute metrics validation by comparing column metadata.

        Args:
            table_context: Table configuration containing all necessary validation parameters

        Returns:
            bool: True if validation passes, False otherwise

        """
        LOGGER.info(
            "Starting metrics validation for table: %s",
            table_context.fully_qualified_name,
        )

        extraction_message = (
            f"Extracting Metrics metadata for: "
            f"{table_context.fully_qualified_name} on {{}}"
        )

        self.context.output_handler.handle_message(
            message=extraction_message.format(self.context.source_platform.value),
            level=OutputMessageLevel.INFO,
        )
        LOGGER.debug("Extracting source metrics metadata")
        source_metadata = self.source_extractor.extract_metrics_metadata(
            table_context=table_context,
            metrics_templates=self.context.source_templates.metrics_templates,
            context=self.context,
        )

        self.context.output_handler.handle_message(
            message=extraction_message.format(self.context.target_platform.value),
            level=OutputMessageLevel.INFO,
        )
        LOGGER.debug("Extracting target metrics metadata")
        target_metadata = self.target_extractor.extract_metrics_metadata(
            table_context=table_context,
            metrics_templates=self.context.target_templates.metrics_templates,
            context=self.context,
        )

        LOGGER.debug("Validating metrics metadata")
        validation_result = data_validator.validate_column_metadata(
            object_name=table_context.fully_qualified_name,
            target_df=target_metadata,
            source_df=source_metadata,
            context=self.context,
        )
        validation_status = "passed" if validation_result else "failed"
        LOGGER.info(
            "Metrics validation %s for table: %s",
            validation_status,
            table_context.fully_qualified_name,
        )
        self.context.output_handler.handle_message(
            header=f"Metrics validation {validation_status}.",
            message="",
            level=OutputMessageLevel.SUCCESS
            if validation_result
            else OutputMessageLevel.FAILURE,
        )
        return validation_result

    @validation_handler("Row validation failed.")
    @log
    def execute_row_validation(
        self,
        table_context: TableConfiguration,
    ) -> bool:
        """Execute row validation (placeholder implementation).

        Args:
            table_context: Table configuration containing all necessary validation parameters

        Returns:
            bool: True (placeholder - row validation not yet implemented)

        """
        LOGGER.info(
            "Starting row validation for table: %s", table_context.fully_qualified_name
        )
        # Placeholder - row validation not implemented yet
        LOGGER.warning("Row validation not yet implemented - skipping")
        self.context.output_handler.handle_message(
            header="Row validation skipped.",
            message="Row validation is not yet implemented.",
            level=OutputMessageLevel.INFO,
        )
        return True

    def _get_schema_validation_message(self, table_context: TableConfiguration) -> str:
        """Get sync validation message for schema validation."""
        return (
            f"Validating schema for {table_context.fully_qualified_name} "
            f"with columns {table_context.column_selection_list}."
        )

    def _get_metrics_validation_message(self, table_context: TableConfiguration) -> str:
        """Get sync validation message for metrics validation."""
        return (
            f"Validating metrics for {table_context.fully_qualified_name} "
            f"with columns {table_context.column_selection_list}."
        )

    def _get_row_validation_message(self, table_context: TableConfiguration) -> str:
        """Get sync validation message for row validation."""
        return (
            f"Validating rows for {table_context.fully_qualified_name} "
            f"with columns {table_context.column_selection_list}."
        )
