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
        # In a real implementation, we would validate the workspace
        # For now, we'll simulate success with a mock workspace
        mock_workspace = {
            "id": "1" if workspace == "default" else "2",
            "name": workspace,
        }
        
        ctx.obj = {
            "workspace": mock_workspace,
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
def upload_schemas(
    ctx: typer.Context,
    schema_dir: Path = typer.Argument(
        ...,
        help="Path to the directory containing schema files to upload",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    pattern: str = typer.Option(
        "*.json",
        help="File pattern to match schema files in the directory",
    ),
) -> None:
    """Upload or update schemas from files in a specified directory."""
    try:
        workspace = ctx.obj["workspace"]
        
        # In a real implementation, we would read and upload the actual schema files
        # For now, we'll simulate the process
        
        # Simulate finding schema files in the directory
        import glob
        
        schema_files = list(schema_dir.glob(pattern))
        
        if not schema_files:
            panel = get_argilla_themed_panel(
                f"No schema files matching '{pattern}' found in {schema_dir}",
                title="No schemas found",
                title_align="left",
                success=False,
            )
            Console().print(panel)
            raise typer.Exit(code=1)
        
        # Process each schema file
        uploaded_count = 0
        updated_count = 0
        
        for schema_file in schema_files:
            # Simulate processing and uploading
            # In a real implementation, we would read and parse the file
            file_name = schema_file.name
            
            # Mock processing logic - alternate between upload and update
            if uploaded_count % 2 == 0:
                # Simulate new schema
                result = "uploaded"
                uploaded_count += 1
            else:
                # Simulate updated schema
                result = "updated"
                updated_count += 1
                
            panel = get_argilla_themed_panel(
                f"Schema '{file_name}' {result} successfully",
                title=f"Schema {result.capitalize()}",
                title_align="left",
            )
            Console().print(panel)
        
        # Final summary
        total_count = uploaded_count + updated_count
        panel = get_argilla_themed_panel(
            f"Processed {total_count} schema files\n"
            f"• New schemas: {uploaded_count}\n"
            f"• Updated schemas: {updated_count}\n"
            f"• Workspace: {workspace['name']}",
            title="Upload Complete",
            title_align="left",
        )
        Console().print(panel)
        
    except Exception as e:
        panel = get_argilla_themed_panel(
            f"An unexpected error occurred when uploading schemas: {str(e)}",
            title="Upload Failed",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="list", help="List schemas")
def list_schemas(
    ctx: typer.Context,
    name: Optional[str] = typer.Option(None, help="Filter schemas by name"),
) -> None:
    """List available schemas with optional filtering."""
    try:
        workspace = ctx.obj["workspace"]
        
        # In a real implementation, we would fetch schemas from the server
        # For now, we'll use mock data
        schemas = get_mock_schemas()
        
        # Apply filter if specified
        if name:
            schemas = [s for s in schemas if name.lower() in s["name"].lower()]
        
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
        
        # In a real implementation, we would delete the schema via the API
        # For now, we'll simulate this process
        
        # Check if the schema exists
        schemas = get_mock_schemas()
        schema = next((s for s in schemas if s["id"] == schema_id), None)
        
        if not schema:
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
        
        # Simulate deletion
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
