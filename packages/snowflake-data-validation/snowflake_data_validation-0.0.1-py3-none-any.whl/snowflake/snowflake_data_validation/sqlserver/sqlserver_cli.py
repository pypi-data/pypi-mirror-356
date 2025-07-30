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
"""SQL Server CLI commands for data validation."""

import contextlib

from functools import wraps
from pathlib import Path
from typing import Annotated, Optional

import typer

from snowflake.snowflake_data_validation.comparison_orchestrator import (
    ComparisonOrchestrator,
)
from snowflake.snowflake_data_validation.configuration.configuration_loader import (
    ConfigurationLoader,
)
from snowflake.snowflake_data_validation.sqlserver.sqlserver_arguments_manager import (
    SqlServerArgumentsManager,
)
from snowflake.snowflake_data_validation.utils.arguments_manager_factory import (
    create_validation_environment_from_config,
)
from snowflake.snowflake_data_validation.utils.console_output_handler import (
    ConsoleOutputHandler,
)
from snowflake.snowflake_data_validation.utils.constants import (
    CREDENTIALS_CONNECTION_MODE,
    ExecutionMode,
    Platform,
)


# Create SQL Server typer app
sqlserver_app = typer.Typer()


@contextlib.contextmanager
def managed_validation_environment(env=None):
    """Context manager for validation environment cleanup."""
    try:
        yield env
    finally:
        if env:
            env.cleanup()


def handle_validation_errors(func):
    """Handle validation errors and provide user-friendly messages."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except typer.BadParameter as e:
            typer.secho(f"Invalid parameter: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1) from None
        except FileNotFoundError as e:
            typer.secho(
                f"Configuration file not found: {e}", fg=typer.colors.RED, err=True
            )
            raise typer.Exit(1) from None
        except ConnectionError as e:
            typer.secho(f"Connection error: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1) from None
        except Exception as e:
            typer.secho(f"Operation failed: {e}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1) from None

    return wrapper


def create_environment_from_config(
    data_validation_config_file: str,
    execution_mode: ExecutionMode,
    console_output: bool = True,
):
    """Create validation environment from configuration file."""
    config_path = Path(data_validation_config_file)
    config_loader = ConfigurationLoader(config_path)
    config_model = config_loader.get_configuration_model()

    return create_validation_environment_from_config(
        config_model=config_model,
        data_validation_config_file=data_validation_config_file,
        execution_mode=execution_mode,
        output_handler=ConsoleOutputHandler(enable_console_output=console_output),
    )


def build_snowflake_credentials(
    account: Optional[str] = None,
    username: Optional[str] = None,
    database: Optional[str] = None,
    schema: Optional[str] = None,
    warehouse: Optional[str] = None,
    role: Optional[str] = None,
    authenticator: Optional[str] = None,
    password: Optional[str] = None,
) -> dict[str, str]:
    """Build Snowflake credentials dictionary from parameters."""
    credentials = {}
    if account:
        credentials["account"] = account
    if username:
        credentials["username"] = username
    if database:
        credentials["database"] = database
    if schema:
        credentials["schema"] = schema
    if warehouse:
        credentials["warehouse"] = warehouse
    if role:
        credentials["role"] = role
    if authenticator:
        credentials["authenticator"] = authenticator
    if password:
        credentials["password"] = password

    return credentials


@sqlserver_app.command("run-validation")
@handle_validation_errors
def sqlserver_run_validation(
    data_validation_config_file: Annotated[
        str,
        typer.Option(
            "--data-validation-config-file",
            "-dvf",
            help="Data validation configuration file path. ",
        ),
    ],
):
    """Run data validation for SQL Server to Snowflake."""
    typer.secho("Starting SQL Server to Snowflake validation...", fg=typer.colors.BLUE)

    # Create validation environment from config file
    validation_env = create_environment_from_config(
        data_validation_config_file, ExecutionMode.SYNC_VALIDATION
    )
    with managed_validation_environment(validation_env) as validation_env:
        orchestrator = ComparisonOrchestrator.from_validation_environment(
            validation_env
        )
        orchestrator.run_sync_comparison()
        typer.secho("Validation completed successfully!", fg=typer.colors.GREEN)


@sqlserver_app.command("run-async-validation")
@handle_validation_errors
def sqlserver_run_async_validation(
    data_validation_config_file: Annotated[
        str,
        typer.Option(
            "--data-validation-config-file",
            "-dvf",
            help="Data validation configuration file path. ",
        ),
    ],
):
    """Run async data validation for SQL Server to Snowflake."""
    typer.secho(
        "Starting SQL Server to Snowflake async validation...", fg=typer.colors.BLUE
    )

    validation_env = create_environment_from_config(
        data_validation_config_file, ExecutionMode.ASYNC_VALIDATION
    )
    with managed_validation_environment(validation_env) as validation_env:
        orchestrator = ComparisonOrchestrator.from_validation_environment(
            validation_env
        )
        orchestrator.run_async_comparison()
        typer.secho("Validation completed successfully!", fg=typer.colors.GREEN)


@sqlserver_app.command("run-validation-ipc", hidden=True)
@handle_validation_errors
def sqlserver_run_validation_ipc(
    source_host: Annotated[
        str, typer.Option("--source-host", "-srch", help="Source Host name")
    ],
    source_port: Annotated[
        int, typer.Option("--source-port", "-srcp", help="Source Port number")
    ],
    source_username: Annotated[
        str, typer.Option("--source-username", "-srcu", help="Source Username")
    ],
    source_password: Annotated[
        str, typer.Option("--source-password", "-srcpw", help="Source Password")
    ],
    source_database: Annotated[
        str, typer.Option("--source-database", "-srcd", help="Source Database used")
    ],
    snow_account: Annotated[
        str, typer.Option("--snow-account", "-sa", help="Snowflake account name")
    ] = None,
    snow_username: Annotated[
        str, typer.Option("--snow_username", "-su", help="Snowflake Username")
    ] = None,
    snow_database: Annotated[
        str, typer.Option("--snow_database", "-sd", help="Snowflake Database used")
    ] = None,
    snow_schema: Annotated[
        str, typer.Option("--snow_schema", "-ss", help="Snowflake Schema used")
    ] = None,
    snow_warehouse: Annotated[
        str, typer.Option("--snow_warehouse", "-sw", help="Snowflake Warehouse used")
    ] = None,
    snow_role: Annotated[
        str, typer.Option("--snow_role", "-sr", help="Snowflake Role used")
    ] = None,
    snow_authenticator: Annotated[
        str,
        typer.Option(
            "--snow_authenticator", "-sau", help="Snowflake Authenticator method used"
        ),
    ] = None,
    snow_password: Annotated[
        str, typer.Option("--snow_password", "-sp", help="Snowflake Password")
    ] = None,
    data_validation_config_file: Annotated[
        str,
        typer.Option(
            "--data-validation-config-file",
            "-dvf",
            help="Data validation configuration file path.",
        ),
    ] = None,
):
    """Run data validation for SQL Server to Snowflake with IPC (In-Process Communication).

    This command allows direct specification of connection parameters without requiring
    pre-saved connection files.
    """
    # Set up arguments manager and connections
    args_manager = SqlServerArgumentsManager()

    # Set up sqlserver connection source
    source_connector = args_manager.setup_source_connection(
        source_host=source_host,
        source_port=source_port,
        source_username=source_username,
        source_password=source_password,
        source_database=source_database,
    )

    # Build Snowflake credentials target
    snow_credential_object = build_snowflake_credentials(
        account=snow_account,
        username=snow_username,
        database=snow_database,
        schema=snow_schema,
        warehouse=snow_warehouse,
        role=snow_role,
        authenticator=snow_authenticator,
        password=snow_password,
    )

    # Set up target connection
    target_connector = args_manager.setup_target_connection(
        snowflake_conn_mode=CREDENTIALS_CONNECTION_MODE,
        snow_credential_object=snow_credential_object
        if snow_credential_object
        else None,
    )

    configuration = args_manager.load_configuration(
        data_validation_config_file=data_validation_config_file
    )

    with managed_validation_environment() as validation_env:
        # Set up validation environment
        validation_env = args_manager.setup_validation_environment(
            source_connector=source_connector,
            target_connector=target_connector,
            data_validation_config_file=data_validation_config_file,
            output_directory_path=configuration.output_directory_path,
            output_handler=ConsoleOutputHandler(enable_console_output=False),
        )

        orchestrator = ComparisonOrchestrator.from_validation_environment(
            validation_env
        )
        orchestrator.run_sync_comparison()
        typer.secho("Validation completed successfully!", fg=typer.colors.GREEN)


@sqlserver_app.command("generate-validation-scripts")
@handle_validation_errors
def sqlserver_run_async_generation(
    data_validation_config_file: Annotated[
        str,
        typer.Option(
            "--data-validation-config-file",
            "-dvf",
            help="Data validation configuration file path. ",
        ),
    ],
):
    """Generate validation scripts for SQL Server to Snowflake.

    This command uses ScriptWriter instances to write SQL queries to files
    instead of executing them for validation.
    """
    typer.secho(
        "Starting SQL Server to Snowflake validation script generation...",
        fg=typer.colors.BLUE,
    )

    validation_env = create_environment_from_config(
        data_validation_config_file, ExecutionMode.ASYNC_GENERATION
    )
    with managed_validation_environment(validation_env) as validation_env:
        orchestrator = ComparisonOrchestrator.from_validation_environment(
            validation_env
        )
        orchestrator.run_async_generation()
        typer.secho("Validation scripts generated successfully!", fg=typer.colors.GREEN)


@sqlserver_app.command(
    "get-configuration-files", help="Get configuration files for SQL Server validation."
)
def sqlserver_get_configuration_files(
    templates_directory: Annotated[
        Optional[str],
        typer.Option(
            "--templates-directory",
            "-td",
            help="Directory to save the configuration templates.",
        ),
    ]
):
    """Get configuration files for SQL Server validation."""
    try:
        typer.secho(
            "Retrieving SQL Server validation configuration files...",
            fg=typer.colors.BLUE,
        )
        args_manager = SqlServerArgumentsManager()
        args_manager.dump_and_write_yaml_templates(
            source=Platform.SQLSERVER.value, templates_directory=templates_directory
        )
        typer.secho("Configuration files were generated ", fg=typer.colors.GREEN)
    except PermissionError as e:
        raise RuntimeError(
            f"Permission denied while writing template files: {e}"
        ) from e
    except Exception as e:
        raise RuntimeError(f"Failed to generate configuration files: {e}") from e
