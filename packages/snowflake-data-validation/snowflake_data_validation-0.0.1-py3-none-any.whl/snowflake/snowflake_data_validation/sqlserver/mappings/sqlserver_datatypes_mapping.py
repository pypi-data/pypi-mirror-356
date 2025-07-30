# Copyright 2025 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0

"""SQL Server to target platform datatype mapping functionality."""

import logging

from snowflake.snowflake_data_validation.mappings.datatypes_mapping_base import (
    BaseDataTypeMapper,
)
from snowflake.snowflake_data_validation.utils.constants import Platform


logger = logging.getLogger(__name__)


class SQLServerDataTypeMapper(BaseDataTypeMapper):

    """SQLServer specific implementation of the BaseDataTypeMapper."""

    _instance = None

    def __new__(
        cls, template_path: str, target_platform: str
    ) -> "SQLServerDataTypeMapper":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__(template_path, target_platform)
        return cls._instance

    @classmethod
    def get_datatype_mappings(
        cls, target_platform: str, template_path: str
    ) -> dict[str, str]:
        """Get the datatype mappings for SQLServer to target platform.

        Args:
            target_platform (str): The target platform to get mappings for.
            template_path (str): Path to the mappings template file.

        Returns:
            dict[str, str]: Dictionary mapping SQLServer datatypes to target platform datatypes

        """
        instance = cls(template_path, target_platform)
        return instance.mappings

    @property
    def source_column_name(self) -> str:
        """Return the name of the source database column in the mapping template."""
        return Platform.SQLSERVER.value
