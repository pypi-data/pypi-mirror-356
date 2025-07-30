# Copyright 2025 Snowflake Inc.
# SPDX-License-Identifier: Apache-2.0

"""Base class for database datatype mapping functionality."""

import logging

from abc import ABC, abstractmethod
from pathlib import Path

from snowflake.snowflake_data_validation.utils.constants import Platform
from snowflake.snowflake_data_validation.utils.helpers import (
    load_datatypes_templates_from_yaml,
)


logger = logging.getLogger(__name__)


class BaseDataTypeMapper(ABC):

    """Abstract base class for database datatype mappers.

    This class defines the interface for datatype mapping functionality across different
    database systems. Each concrete implementation should handle its own singleton pattern
    if needed.

    Args:
        template_path (str): Path to the mappings template file.
        target_platform (str): The target platform to use for mappings.

    """

    def __init__(
        self, template_path: str, target_platform: str = Platform.SNOWFLAKE.value
    ) -> None:
        """Initialize the mapper with the provided template path and target platform.

        Args:
            template_path (str): Path to the mappings template file.
            target_platform (str): The target platform to use for mappings.

        """
        self._template_path = Path(template_path)
        self._mappings = self._load_mappings(target_platform.lower())

    @property
    @abstractmethod
    def source_column_name(self) -> str:
        """Return the name of the source database column in the mapping template."""
        pass

    @property
    def mappings(self) -> dict[str, str]:
        """Get the current datatype mappings.

        Returns:
            dict[str, str]: Dictionary mapping source datatypes to target platform datatypes

        """
        return self._mappings.copy()

    def _load_mappings(self, target_platform: str) -> dict[str, str]:
        """Load datatype mappings from CSV file for a specific target platform.

        Args:
            target_platform (str): The target platform to get mappings for.
                                Currently only supports 'snowflake'.

        Returns:
            dict[str, str]: Dictionary mapping source datatypes to target platform datatypes

        Raises:
            FileNotFoundError: If the mapping template file does not exist
            ValueError: If target_platform is not supported or target column not found in CSV

        """
        df = load_datatypes_templates_from_yaml(
            self._template_path, self.source_column_name
        )
        source_col = self.source_column_name.lower()
        target_platform = target_platform.lower()

        # Convert column names to lowercase
        df.columns = df.columns.str.lower()

        if target_platform not in df.columns:
            available_platforms = [col for col in df.columns if col != source_col]
            raise ValueError(
                f"Target platform '{target_platform}' not supported. "
                f"Available platforms: {available_platforms}"
            )

        df_filtered = df[[source_col, target_platform]].dropna()
        return df_filtered.set_index(source_col)[target_platform].to_dict()
