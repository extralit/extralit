"""Download schemas from a workspace."""

import os
import sys
import json
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from argilla.client import Argilla
from argilla.cli.rich import get_argilla_themed_panel


def download_schemas(
    ctx: typer.Context,
    output_dir: Path = typer.Argument(
        ...,
        help="Directory to save the downloaded schemas",
        file_okay=False,
        dir_okay=True,
        writable=True,
    ),
    name: Optional[str] = typer.Option(
        None,
        "--name",
        "-n",
        help="Filter schemas by name",
    ),
    exclude: Optional[List[str]] = typer.Option(
        None,
        "--exclude",
        "-e",
        help="List of schema names to exclude from download",
    ),
    overwrite: bool = typer.Option(
        False,
        "--overwrite",
        "-o",
        help="Overwrite existing schema files",
    ),
) -> None:
    """Download schemas from a workspace."""
    console = Console()

    try:
        # Get client and workspace from context
        client = ctx.obj["client"]
        workspace = ctx.obj["workspace"]

        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        # Get the workspace object
        workspace_obj = client.workspaces(name=workspace["name"])
        if not workspace_obj:
            panel = get_argilla_themed_panel(
                f"Workspace '{workspace['name']}' not found.",
                title="Workspace not found",
                title_align="left",
                success=False,
            )
            console.print(panel)
            raise typer.Exit(code=1)

        # Get schemas from the workspace
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(f"Fetching schemas from workspace '{workspace['name']}'...", total=None)
            
            # Get schemas
            schemas = workspace_obj.get_schemas()
            
            progress.update(task, completed=True, description=f"Fetched schemas from workspace '{workspace['name']}'")

        if not schemas.schemas:
            panel = get_argilla_themed_panel(
                f"No schemas found in workspace '{workspace['name']}'.",
                title="No schemas found",
                title_align="left",
                success=True,
            )
            console.print(panel)
            return

        # Filter schemas by name if provided
        if name:
            schemas.schemas = [schema for schema in schemas.schemas if name.lower() in schema.name.lower()]

        # Filter out excluded schemas
        if exclude:
            schemas.schemas = [schema for schema in schemas.schemas if schema.name not in exclude]

        if not schemas.schemas:
            panel = get_argilla_themed_panel(
                f"No schemas found in workspace '{workspace['name']}' after applying filters.",
                title="No schemas found",
                title_align="left",
                success=True,
            )
            console.print(panel)
            return

        # Download each schema
        downloaded_schemas = []
        for schema in schemas.schemas:
            output_file = output_dir / f"{schema.name}.json"
            
            # Check if file exists and skip if not overwriting
            if output_file.exists() and not overwrite:
                console.print(f"[yellow]Skipping schema '{schema.name}': File already exists[/yellow]")
                continue
            
            # Save the schema to file
            with open(output_file, "w") as f:
                f.write(schema.to_json())
            
            downloaded_schemas.append(schema.name)

        if not downloaded_schemas:
            panel = get_argilla_themed_panel(
                f"No schemas were downloaded from workspace '{workspace['name']}'.",
                title="No schemas downloaded",
                title_align="left",
                success=False,
            )
            console.print(panel)
            return

        # Show success message
        panel = get_argilla_themed_panel(
            f"Successfully downloaded {len(downloaded_schemas)} schema(s) from workspace '{workspace['name']}' to '{output_dir}'.",
            title="Schemas downloaded",
            title_align="left",
            success=True,
        )
        console.print(panel)

        # List downloaded schemas
        console.print(f"\nDownloaded schemas:")
        for schema_name in downloaded_schemas:
            console.print(f"  - {schema_name}")

    except Exception as e:
        panel = get_argilla_themed_panel(
            f"Error downloading schemas: {str(e)}",
            title="Error",
            title_align="left",
            success=False,
        )
        console.print(panel)
        raise typer.Exit(code=1)
