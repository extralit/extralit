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

from typing import Optional, Dict, Any, List, TYPE_CHECKING
from enum import Enum

import typer

from argilla.cli.callback import init_callback
from argilla.cli.rich import get_argilla_themed_panel
from rich.console import Console
from rich.table import Table

if TYPE_CHECKING:
    from argilla.client.core import Argilla


_COMMANDS_REQUIRING_DATASET = ["delete", "push-to-huggingface"]


def callback(
    ctx: typer.Context,
    name: Optional[str] = typer.Option(None, help="The name of the dataset to which apply the command"),
    workspace: Optional[str] = typer.Option(None, help="The name of the workspace where the dataset belongs"),
) -> None:
    """Callback for dataset commands."""
    client = init_callback()

    if ctx.invoked_subcommand not in _COMMANDS_REQUIRING_DATASET:
        return

    if name is None:
        raise typer.BadParameter(
            f"The command requires a dataset name provided using '--name' option before the {typer.style(ctx.invoked_subcommand, bold=True)} keyword"
        )

    try:
        dataset = client(name=name, workspace=workspace)
        ctx.obj = dataset
    except ValueError as e:
        panel = get_argilla_themed_panel(
            str(e),
            title="Dataset not found",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(1)
    except Exception as e:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to get the dataset from the Extralit server.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


app = typer.Typer(help="Commands for dataset management", no_args_is_help=True, callback=callback)


@app.command(name="list", help="List datasets linked to user's workspaces")
def list_datasets(
    workspace: str = typer.Option(None, help="Filter datasets by workspace"),
) -> None:
    """List datasets with optional filtering by workspace and type."""
    try:
        client = init_callback()

        datasets = client.datasets(workspace=workspace)

        print(datasets)

        # table = Table(title="Datasets", show_lines=True)
        # for column in ("ID", "Name", "Workspace", "Type", "Tags", "Creation Date", "Last Update Date"):
        #     table.add_column(column, justify="center" if column != "Tags" else "left")

        # for dataset in datasets:
        #     # Format tags as bullet points
        #     tags_text = ""
        #     for i, (tag, description) in enumerate(dataset["tags"].items()):
        #         tags_text += f"• [bold]{tag}[/bold]: {description}"
        #         if i < len(dataset["tags"]) - 1:
        #             tags_text += "\n"

        #     table.add_row(
        #         dataset["id"],
        #         dataset["name"],
        #         dataset["workspace"],
        #         str(dataset["type"]),
        #         tags_text,
        #         dataset["created_at"].isoformat(sep=" "),
        #         dataset["updated_at"].isoformat(sep=" "),
        #     )

        # Console().print(table)
    except Exception as e:
        panel = get_argilla_themed_panel(
            f"An unexpected error occurred when trying to list datasets: {str(e)}",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="delete", help="Deletes a dataset")
def delete_dataset(ctx: typer.Context) -> None:
    """Delete a dataset from the system."""
    dataset = ctx.obj

    try:
        # Initialize the client
        client = init_callback()

        # Delete the dataset using the client
        client.delete_dataset(name=dataset["name"], workspace=dataset["workspace"])
        panel = get_argilla_themed_panel(
            f"Dataset with name={dataset['name']} and workspace={dataset['workspace']} deleted successfully",
            title="Dataset deleted",
            title_align="left",
        )
        Console().print(panel)
    except RuntimeError:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to delete the dataset",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="push-to-huggingface", help="Push a dataset to HuggingFace Hub")
def push_to_huggingface(
    ctx: typer.Context,
    repo_id: str = typer.Option(..., help="The HuggingFace Hub repo where the dataset will be pushed to"),
    private: bool = typer.Option(False, help="Whether the dataset should be private or not"),
    token: Optional[str] = typer.Option(None, help="The HuggingFace Hub token to be used for pushing the dataset"),
) -> None:
    """Push a dataset to the HuggingFace Hub."""
    dataset = ctx.obj

    try:
        from rich.live import Live
        from rich.spinner import Spinner

        spinner = Spinner(
            name="dots",
            text=f"Pushing dataset with name={dataset['name']} and workspace={dataset['workspace']} to the"
            " HuggingFace Hub...",
        )

        with Live(spinner, refresh_per_second=20):
            # Initialize the client
            client = init_callback()

            # Push the dataset to HuggingFace Hub
            client.push_dataset_to_huggingface(
                name=dataset["name"],
                repo_id=repo_id,
                private=private,
                token=token,
                workspace=dataset["workspace"]
            )

        panel = get_argilla_themed_panel(
            f"Dataset successfully pushed to the HuggingFace Hub at https://huggingface.co/{repo_id}",
            title="Dataset pushed",
            title_align="left",
        )
        Console().print(panel)
    except ValueError:
        panel = get_argilla_themed_panel(
            "The dataset has no records to push to the HuggingFace Hub. Make sure to add records before"
            " pushing it.",
            title="No records to push",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(1)
    except Exception:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to push the dataset to the HuggingFace Hub",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="create", help="Creates a new dataset")
def create_dataset(
    name: str = typer.Option(..., prompt=True, help="The name of the dataset to be created"),
    workspace: Optional[str] = typer.Option(None, help="The workspace where the dataset will be created"),
) -> None:
    """Create a new dataset in the system."""
    try:
        # Initialize the client
        client = init_callback()

        # Create the dataset using the client
        dataset = client.create_dataset(name=name, workspace=workspace)

        # Get the workspace from the created dataset
        workspace = dataset["workspace"]

        panel = get_argilla_themed_panel(
            f"Dataset with name='{name}' successfully created in workspace='{workspace}'.",
            title="Dataset created",
            title_align="left",
        )
        Console().print(panel)
    except ValueError:
        panel = get_argilla_themed_panel(
            f"Dataset with name='{name}' already exists in workspace='{workspace}'.",
            title="Dataset already exists",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)
    except RuntimeError:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to create the dataset.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()