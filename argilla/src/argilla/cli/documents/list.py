"""List documents in a workspace."""

import sys
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from argilla.client import Argilla
from argilla.cli.rich import get_argilla_themed_panel


def list_documents(
    workspace: str = typer.Option(..., "--workspace", "-w", help="Workspace name"),
) -> None:
    """List documents in a workspace."""
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

        # List documents
        documents = workspace_obj.get_documents()

        if not documents:
            panel = get_argilla_themed_panel(
                f"No documents found in workspace '{workspace}'.",
                title="No documents found",
                title_align="left",
                success=True,
            )
            console.print(panel)
            return

        # Create a table to display the documents
        table = Table(title=f"Documents in workspace '{workspace}'")
        table.add_column("ID", style="cyan")
        table.add_column("URL", style="green")
        table.add_column("PMID", style="yellow")
        table.add_column("DOI", style="blue")
        table.add_column("Created", style="magenta")
        table.add_column("Updated", style="magenta")

        # Add documents to the table
        for doc in documents:
            # Format the dates
            inserted_at = doc.inserted_at.strftime("%Y-%m-%d %H:%M:%S") if doc.inserted_at else "N/A"
            updated_at = doc.updated_at.strftime("%Y-%m-%d %H:%M:%S") if doc.updated_at else "N/A"

            # Add the row
            table.add_row(
                str(doc.id) if doc.id else "N/A",
                doc.url or "N/A",
                doc.pmid or "N/A",
                doc.doi or "N/A",
                inserted_at,
                updated_at,
            )

        # Print the table
        console.print(table)

        # Print a success message
        panel = get_argilla_themed_panel(
            f"Found {len(documents)} documents in workspace '{workspace}'.",
            title="Documents listed successfully",
            title_align="left",
            success=True,
        )
        console.print(panel)

    except Exception as e:
        panel = get_argilla_themed_panel(
            f"Error listing documents: {str(e)}",
            title="Error",
            title_align="left",
            success=False,
        )
        console.print(panel)
        raise typer.Exit(code=1)
