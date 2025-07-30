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


import pandas as pd

from snowflake.snowflake_data_validation.configuration.model.table_configuration import (
    TableConfiguration,
)
from snowflake.snowflake_data_validation.connector.connector_base import (
    ConnectorBase,
)
from snowflake.snowflake_data_validation.extractor.metadata_extractor_base import (
    MetadataExtractorBase,
)
from snowflake.snowflake_data_validation.query.query_generator_base import (
    QueryGeneratorBase,
)
from snowflake.snowflake_data_validation.utils.base_output_handler import (
    OutputMessageLevel,
)
from snowflake.snowflake_data_validation.utils.constants import (
    COLUMN_VALIDATED,
    Platform,
)
from snowflake.snowflake_data_validation.utils.context import Context
from snowflake.snowflake_data_validation.utils.helpers import (
    get_decomposed_fully_qualified_name,
)


class MetadataExtractorSQLServer(MetadataExtractorBase):

    """Implement methods to extract metadata from SQLServer database tables."""

    def __init__(
        self,
        connector: ConnectorBase,
        query_generator: QueryGeneratorBase,
        report_path: str = "",
    ):
        """Initialize the SQLServer metadata extractor with a SQLServer connector.

        Args:
            connector (ConnectorSqlServer): SQLServer database connector instance.
            query_generator: Query generator instance for generating SQL queries.
            report_path (str): Path to save the metadata extraction report.

        """
        super().__init__(connector, query_generator, report_path)

    def extract_schema_metadata(
        self,
        table_context: TableConfiguration,
        context: Context,
    ) -> pd.DataFrame:
        """Extract metadata for a specified table from a SQL Server database.

        Args:
            table_context (TableConfiguration): Configuration object containing table properties.
            context (Context): The execution context containing relevant configuration and runtime information.

        Returns:
            pd.DataFrame: A DataFrame containing the metadata information of the specified table.

        Raises:
            ValueError: If the fully qualified name is not in the correct format.
            DatabaseError: If there is an error executing the SQL query.

        """
        sql_query = self.query_generator.generate_schema_query(table_context, context)

        result = self.connector.execute_query(sql_query)
        if not result:
            return pd.DataFrame()
        columns_names, metadata_info = result

        if not metadata_info:
            context.output_handler.handle_message(
                message=f"No metadata found for table: {table_context.fully_qualified_name}",
                level=OutputMessageLevel.WARNING,
            )
            return pd.DataFrame()

        return self._process_query_result_to_dataframe(
            columns_names=columns_names,
            data_rows=metadata_info,
            context=context,
            header="SQL Server metadata info:",
            output_level=OutputMessageLevel.SOURCE_RESULT,
            apply_column_validated_uppercase=True,
            sort_and_reset_index=True,
        )

    def extract_metrics_metadata(
        self,
        table_context: TableConfiguration,
        metrics_templates: pd.DataFrame,
        context: Context,
    ) -> pd.DataFrame:
        """Extract column-level metadata for all columns in the specified SQL Server table.

        Args:
            table_context (TableConfiguration): Configuration object containing table properties.
            metrics_templates (pd.DataFrame): DataFrame containing metrics templates to be applied.
            context (Context): The execution context containing relevant configuration and runtime information.

        Returns:
            pd.DataFrame: A DataFrame containing column metadata including data type, statistics, etc.

        """
        query = self.query_generator.generate_metrics_query(
            table_context, metrics_templates, context, self.connector
        )
        result_columns, result = self.connector.execute_query(query)

        return self._process_query_result_to_dataframe(
            columns_names=result_columns,
            data_rows=result,
            context=context,
            header="SQL Server column metrics info:",
            output_level=OutputMessageLevel.SOURCE_RESULT,
            apply_column_validated_uppercase=True,
            sort_and_reset_index=True,
        )

    def extract_md5_checksum(
        self, fully_qualified_name: str, context: Context
    ) -> pd.DataFrame:
        """Extract the MD5 checksum for a given table in SQL Server.

        This method calculates the MD5 checksum for the specified table by
        concatenating all column values into a single string, ensuring consistent
        ordering by converting the values into a JSON array format. The checksum
        is then computed using SQL Server's HASHBYTES function.

        Args:
            fully_qualified_name (str): The fully qualified name of the table
                (e.g., "schema_name.table_name").
            context (Context): The execution context containing relevant
                configuration and runtime information.

        Returns:
            pd.DataFrame: A DataFrame containing the table name and its computed
            MD5 checksum.

        """
        # Implement SQLServer-specific SQL query to extract the table metadata
        # The MD5 checksum will be calculated on the concatenated string of all columns in the table
        # The column values will be converted to a JSON array to ensure consistent ordering
        query = f"""
        SELECT
            '{fully_qualified_name}' as table_name,
            HASHBYTES('MD5', STRING_AGG(CONVERT(NVARCHAR(MAX), t.*), '')) as checksum
        FROM
            {fully_qualified_name} t
        """

        result = self.connector.execute_query(query)
        return pd.DataFrame(result)

    def extract_table_column_metadata(
        self, fully_qualified_name: str, context: Context
    ) -> pd.DataFrame:
        (
            object_database,
            object_schema,
            object_name,
        ) = get_decomposed_fully_qualified_name(fully_qualified_name)

        sql_query = context.sql_generator.extract_table_column_metadata(
            object_database, object_schema, object_name, Platform.SQLSERVER.value
        )

        result_columns, result = self.connector.execute_query(sql_query)

        return self._process_query_result_to_dataframe(
            columns_names=result_columns,
            data_rows=result,
            context=None,
            header=None,
            output_level=None,
            apply_column_validated_uppercase=False,
            sort_and_reset_index=False,
        )

    def _process_query_result_to_dataframe(
        self,
        columns_names: list[str],
        data_rows: list,
        context: Context = None,
        header: str = None,
        output_level: OutputMessageLevel = None,
        apply_column_validated_uppercase: bool = True,
        sort_and_reset_index: bool = True,
    ) -> pd.DataFrame:
        """Process query results into a standardized DataFrame format.

        Args:
            columns_names: List of column names from the query result
            data_rows: List of data rows from the query result
            context: Optional context for output handling
            header: Optional header for output message
            output_level: Optional output message level
            apply_column_validated_uppercase: Whether to apply uppercase to COLUMN_VALIDATED column
            sort_and_reset_index: Whether to sort by all columns and reset index

        Returns:
            pd.DataFrame: Processed DataFrame with standardized formatting

        """
        columns_names_upper = [col.upper() for col in columns_names]
        data_rows_list = [list(row) for row in data_rows]
        df = pd.DataFrame(data_rows_list, columns=columns_names_upper)
        if sort_and_reset_index:
            df = df.sort_values(by=list(df.columns)).reset_index(drop=True)
        if apply_column_validated_uppercase and COLUMN_VALIDATED in df.columns:
            df[COLUMN_VALIDATED] = df[COLUMN_VALIDATED].str.upper()
        if context and header and output_level:
            context.output_handler.handle_message(
                header=header,
                dataframe=df,
                level=output_level,
            )

        return df
