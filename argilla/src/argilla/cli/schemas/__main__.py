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

from typing import Optional, Dict, Any, List
from pathlib import Path
import os
import json

import typer

from argilla.cli.callback import init_callback
from argilla.cli.rich import get_argilla_themed_panel
from rich.console import Console
from rich.table import Table


# Commands that require specific parameters
_COMMANDS_REQUIRING_WORKSPACE = ["upload", "list", "delete"]


def callback(
    ctx: typer.Context,
    workspace: str = typer.Option(
        None,
        "--workspace",
        "-w",
        help="Name of the workspace to which apply the command."
    ),
) -> None:
    """Callback for schema commands."""
    init_callback()

    if ctx.invoked_subcommand not in _COMMANDS_REQUIRING_WORKSPACE:
        return

    if workspace is None:
        raise typer.BadParameter(
            f"The command requires a workspace name provided using '--workspace' option before the {typer.style(ctx.invoked_subcommand, bold=True)} keyword"
        )

    try:
        # Initialize the client
        client = init_callback()

        # Validate the workspace
        from argilla.cli.workspaces.__main__ import get_workspace
        workspace_data = get_workspace(workspace)

        # Store the client and workspace in the context
        ctx.obj = {
            "client": client,
            "workspace": workspace_data,
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
            "An unexpected error occurred when trying to get the workspace.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


app = typer.Typer(help="Commands for schemas management", no_args_is_help=True, callback=callback)


# Mock schemas for demonstration
def get_mock_schemas() -> List[Dict[str, Any]]:
    """Get mock schemas for development."""
    return [
        {
            "id": "schema1",
            "name": "customer-feedback",
            "description": "Schema for customer feedback analysis",
            "version": "1.0.0",
            "created_at": "2025-04-10 15:30:22",
            "updated_at": "2025-04-10 15:30:22"
        },
        {
            "id": "schema2",
            "name": "product-review",
            "description": "Schema for product review analysis",
            "version": "2.1.0",
            "created_at": "2025-04-12 09:45:10",
            "updated_at": "2025-04-13 14:20:15"
        },
        {
            "id": "schema3",
            "name": "support-ticket",
            "description": "Schema for support ticket classification",
            "version": "1.2.3",
            "created_at": "2025-04-14 08:12:55",
            "updated_at": "2025-04-14 08:12:55"
        }
    ]


@app.command(name="upload", help="Upload or update schemas from files in a specified directory")
def upload_schemas_command(
    ctx: typer.Context,
    directory: Path = typer.Argument(
        ...,
        help="Path to the directory containing schema files to upload",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    overwrite: bool = typer.Option(
        False,
        "--overwrite",
        is_flag=True,
        help="Force overwrite of existing schemas in the workspace.",
        show_choices=True,
    ),
    exclude: Optional[List[str]] = typer.Option(
        None,
        "--exclude",
        help="List of schema names to exclude from the update.",
    ),
) -> None:
    """Upload or update schemas from files in a specified directory."""
    # Import the actual implementation from the upload module
    from argilla.cli.schemas.upload import upload_schemas

    # Call the actual implementation
    upload_schemas(ctx, directory, overwrite, exclude)


@app.command(name="list", help="List schemas")
def list_schemas(
    ctx: typer.Context,
    name: Optional[str] = typer.Option(None, help="Filter schemas by name"),
) -> None:
    """List available schemas with optional filtering."""
    try:
        workspace = ctx.obj["workspace"]

        # Get client from context
        client = ctx.obj["client"]

        # Fetch schemas from the server with optional filtering
        schemas = client.list_schemas(workspace=workspace["name"], name=name)

        if not schemas:
            message = f"No schemas found in workspace '{workspace['name']}'"
            if name:
                message += f" matching name '{name}'"

            panel = get_argilla_themed_panel(
                message,
                title="No schemas found",
                title_align="left",
            )
            Console().print(panel)
            return

        # Create and display the table
        table = Table(title=f"Schemas in workspace '{workspace['name']}'")
        table.add_column("ID", justify="left")
        table.add_column("Name", justify="left")
        table.add_column("Description", justify="left")
        table.add_column("Version", justify="center")
        table.add_column("Created", justify="center")
        table.add_column("Updated", justify="center")

        for schema in schemas:
            table.add_row(
                schema["id"],
                schema["name"],
                schema["description"],
                schema["version"],
                schema["created_at"],
                schema["updated_at"],
            )

        Console().print(table)

    except Exception as e:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when listing schemas.",
            title="List Failed",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="delete", help="Delete a schema")
def delete_schema(
    ctx: typer.Context,
    schema_id: str = typer.Argument(..., help="ID of the schema to delete"),
) -> None:
    """Delete a specific schema by ID."""
    try:
        workspace = ctx.obj["workspace"]

        # Get client from context
        client = ctx.obj["client"]

        try:
            # Get the schema to check if it exists and to display its name
            schema = client.get_schema(workspace=workspace["name"], schema_id=schema_id)
        except ValueError:
            panel = get_argilla_themed_panel(
                f"Schema with ID '{schema_id}' not found in workspace '{workspace['name']}'",
                title="Schema not found",
                title_align="left",
                success=False,
            )
            Console().print(panel)
            raise typer.Exit(code=1)

        # Confirmation prompt
        if not typer.confirm(f"Are you sure you want to delete schema '{schema['name']}' ({schema_id})?"):
            panel = get_argilla_themed_panel(
                "Schema deletion cancelled",
                title="Operation Cancelled",
                title_align="left",
            )
            Console().print(panel)
            return

        # Delete the schema via the API
        client.delete_schema(workspace=workspace["name"], schema_id=schema_id)

        # Show success message
        panel = get_argilla_themed_panel(
            f"Schema '{schema['name']}' (ID: {schema_id}) successfully deleted from workspace '{workspace['name']}'",
            title="Schema Deleted",
            title_align="left",
        )
        Console().print(panel)

    except Exception as e:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when deleting the schema.",
            title="Delete Failed",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
