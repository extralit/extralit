"""List files in a workspace."""

import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from argilla.client import Argilla
from argilla.cli.rich import get_argilla_themed_panel


def list_files(
    workspace: str = typer.Option(..., "--workspace", "-w", help="Workspace name"),
    path: str = typer.Option("", "--path", "-p", help="Path prefix to filter files"),
    recursive: bool = typer.Option(True, "--recursive/--no-recursive", help="List files recursively"),
    include_version: bool = typer.Option(True, "--include-version/--no-include-version", help="Include version information"),
) -> None:
    """List files in a workspace."""
    console = Console()

    try:
        # Get the client
        client = Argilla.from_credentials()

        # Get the workspace
        workspace_obj = client.workspaces(name=workspace)
        if not workspace_obj:
            panel = get_argilla_themed_panel(
                f"Workspace '{workspace}' not found.",
                title="Workspace not found",
                title_align="left",
                success=False,
            )
            console.print(panel)
            raise typer.Exit(code=1)

        # List files
        files = workspace_obj.list_files(path, recursive=recursive, include_version=include_version)

        if not files.objects:
            panel = get_argilla_themed_panel(
                f"No files found in workspace '{workspace}' with path prefix '{path}'.",
                title="No files found",
                title_align="left",
                success=True,
            )
            console.print(panel)
            return

        # Create a table to display the files
        table = Table(title=f"Files in workspace '{workspace}'")
        table.add_column("Path", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Last Modified", style="yellow")
        table.add_column("Version ID", style="blue")
        table.add_column("Content Type", style="magenta")

        # Add files to the table
        for file_obj in files.objects:
            # Format the size
            size = file_obj.size
            if size is None:
                size_str = "N/A"
            elif size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.2f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.2f} MB"

            # Format the last modified date
            last_modified = file_obj.last_modified.strftime("%Y-%m-%d %H:%M:%S") if file_obj.last_modified else "N/A"

            # Add the row
            table.add_row(
                file_obj.object_name,
                size_str,
                last_modified,
                file_obj.version_id or "N/A",
                file_obj.content_type or "N/A",
            )

        # Print the table
        console.print(table)

        # Print a success message
        panel = get_argilla_themed_panel(
            f"Found {len(files.objects)} files in workspace '{workspace}'.",
            title="Files listed successfully",
            title_align="left",
            success=True,
        )
        console.print(panel)

    except Exception as e:
        panel = get_argilla_themed_panel(
            f"Error listing files: {str(e)}",
            title="Error",
            title_align="left",
            success=False,
        )
        console.print(panel)
        raise typer.Exit(code=1)
