from pathlib import Path
import os
import glob
from typing import Dict, Optional, List
import typer

def upload_schemas(
    ctx: typer.Context,
    path: Path = typer.Argument(
        ...,
        help="The directory containing the JSON schema files to be updated to the Workspace files.",
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
    from argilla.cli.rich import get_argilla_themed_panel
    from rich.console import Console
    from rich.table import Table

    console = Console()

    try:
        # Get client and workspace from context
        client = ctx.obj["client"]
        workspace = ctx.obj["workspace"]
        
        # Find all JSON files in the directory
        schema_files = glob.glob(os.path.join(path, "*.json"))
        
        if not schema_files:
            panel = get_argilla_themed_panel(
                f"No schema files found in directory '{path}'.",
                title="No schemas found",
                title_align="left",
                success=False,
            )
            console.print(panel)
            raise typer.Exit(code=1)
        
        # Filter out excluded schemas
        if exclude:
            schema_files = [f for f in schema_files if os.path.splitext(os.path.basename(f))[0] not in exclude]
        
        if not schema_files:
            panel = get_argilla_themed_panel(
                f"All schema files in directory '{path}' were excluded.",
                title="No schemas to upload",
                title_align="left",
                success=False,
            )
            console.print(panel)
            raise typer.Exit(code=1)
        
        # Upload each schema file
        uploaded_schemas = []
        for schema_file in schema_files:
            try:
                schema = client.upload_schema(
                    workspace=workspace["name"],
                    schema_file=schema_file,
                    overwrite=overwrite
                )
                uploaded_schemas.append(schema)
            except ValueError as e:
                if "already exists" in str(e) and not overwrite:
                    console.print(f"[yellow]Skipping schema '{os.path.basename(schema_file)}': {str(e)}[/yellow]")
                else:
                    console.print(f"[red]Error uploading schema '{os.path.basename(schema_file)}': {str(e)}[/red]")
            except Exception as e:
                console.print(f"[red]Error uploading schema '{os.path.basename(schema_file)}': {str(e)}[/red]")
        
        if not uploaded_schemas:
            panel = get_argilla_themed_panel(
                f"No schemas were uploaded to workspace '{workspace['name']}'.",
                title="No schemas uploaded",
                title_align="left",
                success=False,
            )
            console.print(panel)
            return
        
        # Show success message
        panel = get_argilla_themed_panel(
            f"Successfully uploaded {len(uploaded_schemas)} schema(s) to workspace '{workspace['name']}'.",
            title="Schemas uploaded",
            title_align="left",
        )
        console.print(panel)
        
        # Create and display the table of uploaded schemas
        table = Table(title=f"Uploaded Schemas in workspace '{workspace['name']}'")
        table.add_column("ID", justify="left")
        table.add_column("Name", justify="left")
        table.add_column("Version", justify="center")
        table.add_column("Created", justify="center")
        table.add_column("Updated", justify="center")
        
        for schema in uploaded_schemas:
            table.add_row(
                schema["id"],
                schema["name"],
                schema["version"],
                schema["created_at"],
                schema["updated_at"],
            )
        
        console.print(table)

    except Exception as e:
        panel = get_argilla_themed_panel(
            f"Unable to update schemas in workspace: {str(e)}", 
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        console.print(panel)
        raise typer.Exit(code=1) from e
