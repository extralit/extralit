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
    from argilla.datasets._resource import Dataset


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
        dataset = client.datasets(name=name, workspace=workspace)
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
            f"An unexpected error occurred when fetching the dataset: {e}",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


app = typer.Typer(help="Commands for dataset management", no_args_is_help=True, callback=callback)


@app.command(name="list", help="List datasets linked to user's workspaces")
def list_datasets(
    workspace: str = typer.Option(..., help="Filter datasets by workspace"),
) -> None:
    """List datasets with optional filtering by workspace and type."""
    try:
        client = init_callback()

        datasets = client.datasets(workspace=workspace)

        table = Table(title="Datasets", show_lines=True)
        for column in ("ID", "Name", "Workspace", "Creation Date", "Last Activity Date"):
            table.add_column(column, justify="center" if column != "Tags" else "left")

        for dataset in datasets:
            table.add_row(
                str(dataset.id),
                dataset.name,
                dataset.workspace.name,
                dataset.inserted_at.isoformat(sep=" "),
                dataset._model.last_activity_at.isoformat(sep=" "),
            )

        Console().print(table)
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
    dataset: "Dataset" = ctx.obj

    try:
        dataset.delete()

        panel = get_argilla_themed_panel(
            f"Dataset with name={dataset.name} and workspace={dataset.workspace.name} deleted successfully",
            title="Dataset deleted",
            title_align="left",
        )
        Console().print(panel)
    except RuntimeError as re:
        panel = get_argilla_themed_panel(
            f"An unexpected error occurred when trying to delete the dataset: {re}",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="push-to-huggingface", help="Push a dataset to HuggingFace Hub", hidden=True)
def push_to_huggingface(
    ctx: typer.Context,
    repo_id: str = typer.Option(..., help="The HuggingFace Hub repo where the dataset will be pushed to"),
    private: bool = typer.Option(False, help="Whether the dataset should be private or not"),
    token: Optional[str] = typer.Option(None, help="The HuggingFace Hub token to be used for pushing the dataset"),
) -> None:
    """Push a dataset to the HuggingFace Hub."""
    dataset: "Dataset" = ctx.obj

    try:
        from rich.live import Live
        from rich.spinner import Spinner

        spinner = Spinner(
            name="dots",
            text=f"Pushing dataset with name={dataset.name} and workspace={dataset.workspace.name} to the"
            " HuggingFace Hub...",
        )

        with Live(spinner, refresh_per_second=20):
            client = init_callback()

            client.push_dataset_to_huggingface(
                name=dataset.name,
                repo_id=repo_id,
                private=private,
                token=token,
                workspace=dataset.workspace
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
    except Exception as e:
        panel = get_argilla_themed_panel(
            f"An unexpected error occurred when trying to push the dataset to the HuggingFace Hub: {e}",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="create", help="Creates a new dataset with configurable settings", hidden=True)
def create_dataset(
    name: str = typer.Option(..., prompt=True, help="The name of the dataset to be created"),
    workspace: str = typer.Option(..., prompt=True, help="The workspace where the dataset will be created"),
    guidelines: Optional[str] = typer.Option(None, prompt=True, help="Guidelines for annotators (optional)"),
    allow_extra_metadata: bool = typer.Option(
        False, prompt=True, help="Whether to allow extra metadata in records"
    ),
    advanced_config: bool = typer.Option(
        False, prompt=True, help="Configure fields and questions interactively"
    ),
) -> None:
    """Create a new dataset with configurable settings in the system."""
    try:
        client = init_callback()
        
        from argilla.settings import Settings, TextField, TextQuestion
        from argilla.datasets._resource import Dataset
        
        fields = [TextField(name="text", title="Text")]
        questions = [TextQuestion(name="comment", title="Comment", description="Add your comments here")]
        
        if advanced_config:
            if typer.confirm("Add a text field?", default=True):
                field_name = typer.prompt("Field name", default="text")
                field_title = typer.prompt("Field title", default="Text")
                fields = [TextField(name=field_name, title=field_title)]
            
            if typer.confirm("Add a text question?", default=True):
                question_name = typer.prompt("Question name", default="comment")
                question_title = typer.prompt("Question title", default="Comment")
                question_desc = typer.prompt("Question description", default="Add your comments here")
                questions = [TextQuestion(name=question_name, title=question_title, description=question_desc)]
        
        settings = Settings(
            fields=fields,
            questions=questions,
            guidelines=guidelines,
            allow_extra_metadata=allow_extra_metadata
        )
        
        dataset = Dataset(
            name=name,
            workspace=workspace,
            settings=settings,
            client=client
        )
        dataset.create()

        panel = get_argilla_themed_panel(
            f"Dataset with name='{name}' successfully created in workspace='{workspace}'.",
            title="Dataset created",
            title_align="left",
        )
        Console().print(panel)
    except ValueError as ve:
        panel = get_argilla_themed_panel(
            f"Dataset creation failed: {ve}",
            title="Dataset creation failed",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)
    except RuntimeError as re:
        panel = get_argilla_themed_panel(
            f"An unexpected error occurred when trying to create the dataset: {re}",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()