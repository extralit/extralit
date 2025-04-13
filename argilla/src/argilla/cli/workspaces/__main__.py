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
from datetime import datetime

import typer

from argilla.cli.callback import init_callback
from argilla.cli.rich import get_argilla_themed_panel
from rich.console import Console
from rich.table import Table


# Helper functions for workspace operations
def get_workspace(name: str) -> Dict[str, Any]:
    """Get a workspace by name."""
    # In a real implementation, we would fetch the workspace from the server
    # For now, we'll simulate success if the name is valid
    workspaces = get_workspaces()
    for workspace in workspaces:
        if workspace["name"] == name:
            return workspace
    raise ValueError(f"Workspace with name={name} does not exist.")


def get_workspaces() -> list[Dict[str, Any]]:
    """Get list of workspaces."""
    # Mock workspaces for development
    return [
        {
            "id": "1",
            "name": "default",
            "inserted_at": datetime.now(),
            "updated_at": datetime.now(),
        },
        {
            "id": "2",
            "name": "research",
            "inserted_at": datetime.now(),
            "updated_at": datetime.now(),
        }
    ]


def get_user(username: str) -> Dict[str, Any]:
    """Get a user by username."""
    # Mock users for development
    users = [
        {
            "id": "1",
            "username": "admin",
            "role": "admin",
            "is_owner": True
        },
        {
            "id": "2",
            "username": "researcher",
            "role": "owner",
            "is_owner": True
        },
        {
            "id": "3",
            "username": "annotator",
            "role": "annotator",
            "is_owner": False
        }
    ]
    
    for user in users:
        if user["username"] == username:
            return user
    
    raise ValueError(f"User with username={username} does not exist.")


# Typer app and callback
_COMMANDS_REQUIRING_WORKSPACE = ["add-user", "delete-user"]


def callback(
    ctx: typer.Context,
    name: Optional[str] = typer.Option(None, help="Name of the workspace to which apply the command."),
) -> None:
    """Callback for workspace commands."""
    init_callback()

    if ctx.invoked_subcommand not in _COMMANDS_REQUIRING_WORKSPACE:
        return

    if name is None:
        raise typer.BadParameter(
            f"The command requires a workspace name provided using '--name' option before the {typer.style(ctx.invoked_subcommand, bold=True)} keyword"
        )

    try:
        workspace = get_workspace(name)
        ctx.obj = workspace
    except ValueError:
        panel = get_argilla_themed_panel(
            f"Workspace with name={name} does not exist.",
            title="Workspace not found",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)
    except RuntimeError:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to get the workspace from the Extralit server",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


app = typer.Typer(help="Commands for workspace management", no_args_is_help=True, callback=callback)


@app.command(name="create", help="Create a workspace")
def create_workspace(
    name: str = typer.Argument(
        ...,
        help="The name of the workspace to be created",
    ),
) -> None:
    """Creates a workspace for the logged user in Extralit."""
    try:
        # In a real implementation, we would create the workspace via the API
        # For now, we'll just simulate success
        panel = get_argilla_themed_panel(
            f"Workspace with the name={name} successfully created.",
            title="Workspace created", 
            title_align="left"
        )
        Console().print(panel)
    except ValueError:
        panel = get_argilla_themed_panel(
            f"Workspace with name={name} already exists.",
            title="Workspace already exists",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)
    except RuntimeError:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to create the workspace.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="list", help="Lists workspaces of the logged user")
def list_workspaces() -> None:
    """List the workspaces in Extralit and prints them on the console."""
    try:
        # In a real implementation, we would fetch workspaces from the server
        # For now, we'll use mock data
        workspaces = get_workspaces()
        
        table = Table(title="Workspaces")
        for column in ("ID", "Name", "Creation Date", "Last Update Date"):
            table.add_column(column, justify="center")

        for workspace in workspaces:
            table.add_row(
                str(workspace["id"]),
                workspace["name"],
                workspace["inserted_at"].isoformat(sep=" "),
                workspace["updated_at"].isoformat(sep=" "),
            )

        Console().print(table)
    except RuntimeError:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to list workspaces.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="add-user", help="Adds a user to a workspace")
def add_user(
    ctx: typer.Context,
    username: str = typer.Argument(..., help="The username of the user to be added to the workspace"),
) -> None:
    """Adds a user to a workspace."""
    workspace = ctx.obj

    try:
        user = get_user(username)

        if user["is_owner"]:
            panel = get_argilla_themed_panel(
                f"User with name={username} is an owner. Users with owner role don't need specific permissions per"
                " workspace, as those are super-users with privileges over everything under Extralit.",
                title="User is owner",
                title_align="left",
                success=False,
            )
            Console().print(panel)
            raise typer.Exit(code=1)

        # In a real implementation, we would add the user to the workspace via the API
        # For now, we'll just simulate success
        panel = get_argilla_themed_panel(
            f"User with username={username} has been added to workspace={workspace['name']}",
            title="User added",
            title_align="left",
        )
        Console().print(panel)
    except ValueError:
        panel = get_argilla_themed_panel(
            f"User with username={username} doesn't exist.",
            title="User not found",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)
    except RuntimeError:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to add user to the workspace.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="delete-user", help="Deletes a user from a workspace")
def delete_user(
    ctx: typer.Context,
    username: str = typer.Argument(..., help="The username of the user to be removed from the workspace"),
) -> None:
    """Removes a user from a workspace."""
    workspace = ctx.obj

    try:
        user = get_user(username)

        if user["is_owner"]:
            panel = get_argilla_themed_panel(
                f"User with name={username} is an owner. Users with owner role don't need specific permissions per"
                " workspace, as those are super-users with privileges over everything under Extralit.",
                title="User is owner",
                title_align="left",
                success=False,
            )
            Console().print(panel)
            raise typer.Exit(code=1)

        # In a real implementation, we would remove the user from the workspace via the API
        # For now, we'll just simulate success
        panel = get_argilla_themed_panel(
            f"User with username={username} has been removed from workspace={workspace['name']}",
            title="User removed",
            title_align="left",
        )
        Console().print(panel)
    except ValueError:
        panel = get_argilla_themed_panel(
            f"User with username={username} doesn't exist.",
            title="User not found",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)
    except RuntimeError:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to remove user from the workspace.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()