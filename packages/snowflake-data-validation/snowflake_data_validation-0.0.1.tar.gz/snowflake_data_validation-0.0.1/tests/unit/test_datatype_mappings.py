import os
import pytest
import pandas as pd
from snowflake.snowflake_data_validation.sqlserver.mappings.sqlserver_datatypes_mapping import (
    SQLServerDataTypeMapper,
)
from snowflake.snowflake_data_validation.utils.constants import (
    Platform,
    SQLSERVER_DATATYPES_MAPPING_TEMPLATE,
)
from .utils.test_constants import SQLServerDataType
from pathlib import Path


@pytest.fixture
def template_path():
    """Provide the path to the test template file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    return os.path.join(
        project_root,
        "src",
        "snowflake",
        "snowflake_data_validation",
        "sqlserver",
        "extractor",
        "templates",
        SQLSERVER_DATATYPES_MAPPING_TEMPLATE,
    )


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset the singleton instance before each test."""
    SQLServerDataTypeMapper._instance = None
    yield
    SQLServerDataTypeMapper._instance = None


def test_load_snowflake_mappings(template_path):
    """Test loading Snowflake datatype mappings."""
    mapper = SQLServerDataTypeMapper(template_path, Platform.SNOWFLAKE.value)
    mappings = mapper.mappings

    # Test some key mappings
    assert mappings[SQLServerDataType.BIGINT] == "NUMBER"
    assert mappings[SQLServerDataType.VARCHAR] == "VARCHAR"
    assert mappings[SQLServerDataType.DATETIME] == "TIMESTAMP_NTZ"
    assert mappings[SQLServerDataType.BINARY] == "BINARY"

    # Test case sensitivity
    assert "bigint" not in mappings  # Should be uppercase only

    # Test dictionary properties with better error messages
    assert len(mappings) > 0, "Mappings dictionary is empty"
    for k, v in mappings.items():
        assert isinstance(
            k, str
        ), f"Mapping key {k!r} is not a string (type: {type(k)})"
        assert isinstance(
            v, str
        ), f"Mapping value {v!r} is not a string (type: {type(v)})"


def test_invalid_platform(template_path):
    """Test loading mappings for an invalid platform."""
    with pytest.raises(ValueError) as exc_info:
        SQLServerDataTypeMapper(template_path, "invalid_platform")

    assert "Target platform 'invalid_platform' not supported" in str(exc_info.value)


def test_empty_mappings(template_path):
    """Test handling of empty target type values in CSV."""
    mapper = SQLServerDataTypeMapper(template_path, Platform.SNOWFLAKE.value)
    mappings = mapper.mappings

    # No mapping should have an empty value with better error message
    for key, value in mappings.items():
        assert value.strip() != "", f"Empty mapping found for SQL Server type: {key}"


def test_all_required_types_present(template_path):
    """Test that all required SQL Server types have mappings."""
    mapper = SQLServerDataTypeMapper(template_path, Platform.SNOWFLAKE.value)
    mappings = mapper.mappings

    # Check each required type with specific error message
    # SQLServerDataType.list() now returns a set, so we need to convert or iterate properly
    required_types = SQLServerDataType.list()
    missing_types = [
        type_name for type_name in required_types if type_name not in mappings
    ]
    assert (
        not missing_types
    ), f"Missing mappings for required SQL Server types: {missing_types}"


def test_file_not_found(monkeypatch):
    """Test handling of missing CSV file."""
    # Reset the singleton instance
    SQLServerDataTypeMapper._instance = None

    with pytest.raises(FileNotFoundError):
        mapper = SQLServerDataTypeMapper(
            "non_existent_file.yaml", Platform.SNOWFLAKE.value
        )
        _ = mapper.mappings


def test_enum_data_types():
    """Test that our enum contains all expected SQL Server data types."""
    data_types = SQLServerDataType.list()

    # Check that we have a reasonable number of data types
    assert (
        len(data_types) >= 30
    ), f"Expected at least 30 data types, got {len(data_types)}"

    # Check some specific data types are present
    expected_types = {
        "BIGINT",
        "VARCHAR",
        "DATETIME",
        "BINARY",
        "INT",
        "FLOAT",
        "DATE",
        "TIME",
        "CHAR",
        "NVARCHAR",
        "DECIMAL",
    }

    missing_expected = expected_types - data_types
    assert not missing_expected, f"Missing expected data types: {missing_expected}"
