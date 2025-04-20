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
    # Get all workspaces and filter by name
    workspaces = get_workspaces()
    for workspace in workspaces:
        if workspace["name"] == name:
            return workspace

    # If we get here, the workspace was not found
    raise ValueError(f"Workspace with name={name} does not exist.")


def get_workspaces() -> list[Dict[str, Any]]:
    """Get list of workspaces."""
    # Initialize the client
    client = init_callback()

    try:
        # Use the proper API client to get workspaces
        workspaces_objects = client.workspaces.list()
        
        # Convert workspace objects to dictionaries with the expected format
        workspaces = []
        for workspace in workspaces_objects:
            workspaces.append({
                "id": str(workspace.id),
                "name": workspace.name,
                "inserted_at": workspace._model.inserted_at if hasattr(workspace._model, 'inserted_at') else datetime.now(),
                "updated_at": workspace._model.updated_at if hasattr(workspace._model, 'updated_at') else datetime.now(),
            })
            
        return workspaces
    except Exception as e:
        # If there's an error, log it and return mock data
        print(f"Warning: Failed to get workspaces: {str(e)}")
        # Fallback to mock data for development
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
    # Initialize the client
    client = init_callback()

    try:
        # Get the user via the proper API client
        user_obj = client.users(username=username)
        
        if not user_obj:
            raise ValueError(f"User with username={username} not found.")
            
        # Convert user object to dictionary with the expected format
        user = {
            "id": str(user_obj.id),
            "username": user_obj.username,
            "role": user_obj.role,
            "first_name": user_obj.first_name if hasattr(user_obj, 'first_name') else "",
            "last_name": user_obj.last_name if hasattr(user_obj, 'last_name') else "",
            "is_owner": user_obj.role in ["admin", "owner"]
        }
        
        return user
    except Exception as e:
        # If there's an error, raise a ValueError
        raise ValueError(f"User with username={username} does not exist: {str(e)}")


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
        # Initialize the client
        client = init_callback()

        # Create a workspace object with the provided name
        from argilla.workspaces import Workspace
        workspace = Workspace(name=name)
        
        # Add the workspace using the proper API
        client.workspaces.add(workspace)

        # Display success message
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
        # Get workspaces from the server
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
    role: str = typer.Option("annotator", help="The role of the user in the workspace (annotator, owner)"),
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

        # Initialize the client
        client = init_callback()
        
        # Get the workspace object
        workspace_obj = client.workspaces(name=workspace['name'])
        if not workspace_obj:
            raise ValueError(f"Workspace with name={workspace['name']} not found.")
            
        # Get the user object
        user_obj = client.users(username=username)
        if not user_obj:
            raise ValueError(f"User with username={username} not found.")
            
        # Add the user to the workspace using the proper API
        from argilla._api._workspaces import WorkspaceUserRole
        workspace_obj.add_user(user=user_obj, role=WorkspaceUserRole(role))

        # Display success message
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

        # Initialize the client
        client = init_callback()
        
        # Get the workspace object
        workspace_obj = client.workspaces(name=workspace['name'])
        if not workspace_obj:
            raise ValueError(f"Workspace with name={workspace['name']} not found.")
            
        # Get the user object
        user_obj = client.users(username=username)
        if not user_obj:
            raise ValueError(f"User with username={username} not found.")
            
        # Remove the user from the workspace using the proper API
        workspace_obj.remove_user(user=user_obj)

        # Display success message
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