from typing import Optional, Union

from pydantic import BaseModel

from snowflake.snowflake_data_validation.configuration.model.connection_types import (
    Connection,
)
from snowflake.snowflake_data_validation.configuration.model.table_configuration import (
    TableConfiguration,
)
from snowflake.snowflake_data_validation.configuration.model.validation_configuration import (
    ValidationConfiguration,
)
from snowflake.snowflake_data_validation.utils.constants import (
    VALIDATION_CONFIGURATION_DEFAULT_VALUE,
)


class ConfigurationModel(BaseModel):

    """Configuration model.

    Args:
        pydantic.BaseModel (pydantic.BaseModel): pydantic BaseModel

    """

    source_platform: str
    target_platform: str
    output_directory_path: str
    parallelization: bool = False
    source_connection: Optional[Connection] = None
    target_connection: Optional[Connection] = None
    source_validation_files_path: Optional[str] = None
    target_validation_files_path: Optional[str] = None
    validation_configuration: ValidationConfiguration = ValidationConfiguration(
        **VALIDATION_CONFIGURATION_DEFAULT_VALUE
    )
    comparison_configuration: Optional[dict[str, Union[str, float]]] = None
    database_mappings: Optional[dict[str, str]] = None
    schema_mappings: Optional[dict[str, str]] = None
    tables: list[TableConfiguration] = []
