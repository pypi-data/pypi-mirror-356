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

from enum import Enum


# ----- PLATFORM ENUMS -----


class Platform(Enum):

    """Enumeration of supported database platforms."""

    SNOWFLAKE = "snowflake"
    SQLSERVER = "sqlserver"


class ExecutionMode(Enum):

    """Enumeration of available execution modes."""

    SYNC_VALIDATION = "sync_validation"
    ASYNC_GENERATION = "async_generation"
    ASYNC_VALIDATION = "async_validation"


class ValidationLevel(Enum):

    """Enumeration of validation level names for the validation report."""

    SCHEMA_VALIDATION = "SCHEMA VALIDATION"
    METRICS_VALIDATION = "METRICS VALIDATION"
    ROW_VALIDATION = "ROW VALIDATION"


# ----- CORE CONSTANTS -----

# Character constants
NEWLINE = "\n"

# Jinja templates names

# Template files
TABLE_METADATA_QUERY = "_table_metadata_query.sql.j2"

# Exception messages
TEMPLATE_NOT_FOUND = (
    "Template not found for platform: {platform}. Please create {template_file} "
    "in the {template_dir} directory."
)
ERROR_GENERATING_TEMPLATE = "Error generating template: {exception}"
CONNECTION_NOT_ESTABLISHED = "Connection is not established. Call connect() first."
FAILED_TO_EXECUTE_QUERY = "An error occurred while executing the query: {query}"
INVALID_CONNECTION_MODE = "Invalid connection mode or missing configuration."

EDITABLE_YAML_FILE_FORMAT_ERROR = r"""Error in the format of {file_name}. Please check the following:
Incorrect indentation: YAML relies heavily on consistent indentation using spaces (not tabs).
Invalid characters: Certain characters might need to be quoted.
Syntax errors in lists or dictionaries: Incorrect use of hyphens for list items or nested structures.
Special characters not quoted: If a string contains special characters it might need to be enclosed in quotes."""

# Temporary constant for data parameters validation
DATA_PARAMETERS = (
    "tables_validate"  # TODO: Remove once Pydantic model implementation is complete
)
FULLY_QUALIFIED_NAME = "fully_qualified_name"
DATA_VALIDATION_CLI = "Data validation CLI"
COLUMN_VALIDATED = "COLUMN_VALIDATED"
COLUMNS_USED_DATA_CONF_FILE = "columns_validate"
COLUMN_DATATYPE = "DATA_TYPE"
DATATYPES_MAPPING_CONF_FILE = "datatype_maping"

# MESSAGES
NOT_EXIST_TARGET = "Not exist in the target"

# Files names
DIFFERENCES_FILE_NAME = "differencesL1.csv"
DIFFERENCES_FILE_NAME2 = "differencesL2.csv"
DATA_VALIDATION_OUTPUT_FOLDER = "output"
DATA_VALIDATION_CONFIGURATION_FILE_YAML = "conf.yaml"
DATA_VALIDATION_CONFIGURATION_FILE_YML = "conf.yml"
DATA_VALIDATION_CONFIGURATION_FILE_NAME = [
    DATA_VALIDATION_CONFIGURATION_FILE_YAML,
    DATA_VALIDATION_CONFIGURATION_FILE_YML,
]
SQLSERVER_DATATYPES_MAPPING_TEMPLATE = "sqlserver_datatypes_mapping_template.yaml"
COLUMN_METRICS_TEMPLATE_NAME_FORMAT = "{platform}_column_metrics_templates.yaml"
COLUMN_DATATYPES_MAPPING_NAME_FORMAT = "{platform}_datatypes_mapping_template.yaml"
TABLE_METADATA_QUERIES_FILENAME = "table_metadata_queries_{timestamp}.sql"
COLUMN_METADATA_QUERIES_FILENAME = "column_metadata_queries_{timestamp}.sql"
COLUMN_NORMALIZARION_TEMPLATE_NAME_FORMAT = (
    "{platform}_column_normalization_templates.yaml"
)
COLUMN_DATATYPES_NORMALIZATION_TEMPLATES_NAME_FORMAT = (
    "{platform}_datatypes_normalization_templates.yaml"
)

# Connection option
DEFAULT_CONNECTION_MODE = "default"
NAME_CONNECTION_MODE = "name"
CREDENTIALS_CONNECTION_MODE = "credentials"
TOML_CONNECTION_MODE = "toml"

# File configuration model constants
SCHEMA_VALIDATION_KEY = "schema_validation"
METRICS_VALIDATION_KEY = "metrics_validation"
COLUMNAR_VALIDATION_KEY = "columnar_validation"
ROW_VALIDATION_KEY = "row_validation"
TOLERANCE_KEY = "tolerance"
TYPE_MAPPING_FILE_PATH_KEY = "type_mapping_file_path"

VALIDATION_CONFIGURATION_DEFAULT_VALUE = {
    SCHEMA_VALIDATION_KEY: True,
    METRICS_VALIDATION_KEY: True,
    COLUMNAR_VALIDATION_KEY: True,
    ROW_VALIDATION_KEY: True,
}

# Column table metadata
CALCULATED_COLUMN_SIZE_IN_BYTES_KEY = "CALCULATED_COLUMN_SIZE_IN_BYTES"
CHARACTER_LENGTH_KEY = "CHARACTER_LENGTH"
COLUMN_NAME_KEY = "COLUMN_NAME"
DATA_TYPE_KEY = "DATA_TYPE"
DATABASE_NAME_KEY = "DATABASE_NAME"
IS_PRIMARY_KEY_KEY = "IS_PRIMARY_KEY"
NULLABLE_KEY = "NULLABLE"
PRECISION_KEY = "PRECISION"
SCALE_KEY = "SCALE"
SCHEMA_NAME_KEY = "SCHEMA_NAME"
TABLE_NAME_KEY = "TABLE_NAME"


COLUMN_VALIDATED = "COLUMN_VALIDATED"

# DATAFRAMES COLUMN NAMES
TYPE_COLUMN_KEY = "type"
METRIC_COLUMN_KEY = "metric"
TEMPLATE_COLUMN_KEY = "template"
NORMALIZATION_COLUMN_KEY = "normalization"

# YAML CONFIGURABLE KEYS
METRIC_QUERY_KEY = "metric_query"
METRIC_NORMALIZATION_KEY = "metric_normalization"
METRIC_RETURN_DATATYPE_KEY = "metric_return_datatype"

# ----- GENERAL CONNECTION FIELD DESCRIPTIONS -----

# General field descriptions that can be reused across different database connections
CONNECTION_NAME_DESC = "The name of the saved connection"
HOST_DESC = "The hostname or IP address of the server"
PORT_DESC = "The port number on which the server is listening"
USERNAME_DESC = "The username for authentication"
PASSWORD_DESC = "The password for authentication"
DATABASE_DESC = "The name of the database to connect to"
