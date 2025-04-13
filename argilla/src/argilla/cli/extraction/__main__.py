# Copyright 2024-present, Argilla, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, Dict, Any
from enum import Enum

import typer

from argilla.cli.callback import init_callback
from argilla.cli.rich import get_argilla_themed_panel
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live


class DatasetType(str, Enum):
    """Dataset types in the system."""
    TEXT_CLASSIFICATION = "text_classification"
    TOKEN_CLASSIFICATION = "token_classification"
    TEXT_GENERATION = "text_generation"
    FEEDBACK = "feedback"


# Commands that require specific parameters
_COMMANDS_REQUIRING_WORKSPACE = ["export"]
_COMMANDS_REQUIRING_ENVFILE = ["export"]


def callback(
    ctx: typer.Context,
    workspace: str = typer.Option(None, help="Name of the workspace to which apply the command."),
    env_file: str = typer.Option(None, help="Path to .env file with environment variables containing S3 credentials."),
) -> None:
    """Callback for extraction commands."""
    init_callback()

    if ctx.invoked_subcommand not in _COMMANDS_REQUIRING_WORKSPACE and ctx.invoked_subcommand not in _COMMANDS_REQUIRING_ENVFILE:
        return

    # Check required parameters based on command
    if ctx.invoked_subcommand in _COMMANDS_REQUIRING_WORKSPACE and workspace is None:
        raise typer.BadParameter(
            f"The command requires a workspace name provided using '--workspace' option before the {typer.style(ctx.invoked_subcommand, bold=True)} keyword"
        )
    
    if ctx.invoked_subcommand in _COMMANDS_REQUIRING_ENVFILE and env_file is None:
        raise typer.BadParameter("The command requires a .env file path provided using '--env-file' option")

    try:
        # In a real implementation, we would validate the workspace and load env file
        # For now, we'll simulate success
        
        # Mock workspace and MinIO client for demonstration
        mock_workspace = {
            "id": "1" if workspace == "default" else "2",
            "name": workspace or "default",
        }
        
        # Simulate loading environment variables from .env file
        if env_file:
            panel = get_argilla_themed_panel(
                f"Loaded environment variables from {env_file}",
                title="Environment Loaded",
                title_align="left",
            )
            Console().print(panel)
        
        # Mock MinIO client
        mock_minio_client = {"connected": True, "endpoint": "mock-s3-endpoint"}
        
        ctx.obj = {
            "workspace": mock_workspace,
            "minio_client": mock_minio_client,
        }
        
    except ValueError as e:
        panel = get_argilla_themed_panel(
            f"Workspace with name={workspace} does not exist.",
            title="Workspace not found",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)
        
    except Exception as e:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to initialize extraction.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


app = typer.Typer(help="Commands for extraction data management", no_args_is_help=True, callback=callback)


@app.command(name="export", help="Export extraction data to S3 storage")
def export_data(
    ctx: typer.Context,
    type_: Optional[DatasetType] = typer.Option(
        None,
        "--type",
        help="The type of datasets to export.",
    ),
    output_path: str = typer.Option(
        "exported-data",
        "--output",
        help="The path where the exported data will be stored.",
    ),
) -> None:
    """Export extraction data to S3 storage."""
    try:
        # In a real implementation, we would fetch and export data
        # For now, we'll simulate the export process
        workspace = ctx.obj["workspace"]
        minio_client = ctx.obj["minio_client"]
        
        # Display export information
        dataset_type = f"({type_.value})" if type_ else "(all types)"
        panel = get_argilla_themed_panel(
            f"Starting export of extraction data for workspace '{workspace['name']}' {dataset_type}",
            title="Export Started",
            title_align="left",
        )
        Console().print(panel)
        
        # Simulate export process
        spinner = Spinner(
            name="dots",
            text="Exporting data...",
        )
        
        import time
        with Live(spinner, refresh_per_second=20):
            # In a real implementation, we would perform the actual export
            # For now, we'll just simulate a delay
            time.sleep(2)  # Simulate export time
        
        # Show completion message
        panel = get_argilla_themed_panel(
            f"Extraction data successfully exported to {output_path}\n"
            f"• Workspace: {workspace['name']}\n"
            f"• Dataset type: {type_.value if type_ else 'All'}\n"
            f"• Storage connection: {minio_client['endpoint']}",
            title="Export Complete",
            title_align="left",
        )
        Console().print(panel)
        
    except Exception as e:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred during data export.",
            title="Export Failed",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="status", help="Check extraction status")
def check_status(
    ctx: typer.Context,
    dataset: Optional[str] = typer.Option(None, help="The name of the dataset to check status for."),
) -> None:
    """Check status of the extraction process."""
    try:
        # In a real implementation, we would check actual extraction status
        # For now, we'll just simulate status information
        
        # Create a mock status table
        from rich.table import Table
        
        table = Table(title="Extraction Status")
        table.add_column("Dataset", justify="left")
        table.add_column("Type", justify="left")
        table.add_column("Status", justify="center")
        table.add_column("Records", justify="right")
        table.add_column("Last Updated", justify="center")
        
        # Add mock data rows
        if dataset:
            # Show status for a specific dataset
            table.add_row(
                dataset,
                "text_classification",
                "✅ Complete",
                "1,250",
                "2025-04-14 12:30:45"
            )
        else:
            # Show status for multiple datasets
            table.add_row(
                "sentiment-analysis",
                "text_classification",
                "✅ Complete",
                "1,250",
                "2025-04-14 12:30:45"
            )
            table.add_row(
                "named-entity-recognition",
                "token_classification",
                "🔄 In Progress (85%)",
                "2,430",
                "2025-04-14 12:35:10"
            )
            table.add_row(
                "text-summarization",
                "text_generation",
                "❌ Failed",
                "0",
                "2025-04-14 11:15:22"
            )
        
        Console().print(table)
        
    except Exception as e:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when checking extraction status.",
            title="Status Check Failed",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
