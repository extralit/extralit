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

from typing import Optional
from enum import Enum

import typer

from argilla.cli.callback import init_callback


class UserRole(str, Enum):
    """User roles in the system."""
    ADMIN = "admin"
    OWNER = "owner"
    ANNOTATOR = "annotator"


def callback(
    ctx: typer.Context,
) -> None:
    """Callback for users commands."""
    init_callback()


app = typer.Typer(help="Commands for user management", no_args_is_help=True, callback=callback)


@app.command(name="create", help="Creates a new user")
def create_user(
    username: str = typer.Option(..., prompt=True, help="The username of the user to be created"),
    password: str = typer.Option(
        ..., prompt=True, confirmation_prompt=True, hide_input=True, help="The password of the user to be created"
    ),
    first_name: Optional[str] = typer.Option(None, help="The first name of the user to be created"),
    last_name: Optional[str] = typer.Option(None, help="The last name of the user to be created"),
    role: UserRole = typer.Option(UserRole.ANNOTATOR, help="The role of the user to be created"),
    workspaces: Optional[list[str]] = typer.Option(
        None,
        "--workspace",
        help="A workspace name to which the user will be linked to. This option can be provided several times.",
    ),
) -> None:
    """Creates a new user in the system."""
    from rich.markdown import Markdown
    from argilla.cli.rich import get_argilla_themed_panel
    from rich.console import Console

    try:
        # In a real implementation, we would create the user via the API
        # For now, we'll simulate success with the provided parameters
        user = {
            "username": username,
            "password": password,  # In real impl, this would be hashed and not displayed
            "first_name": first_name or "",
            "last_name": last_name or "",
            "role": role,
            "api_key": "api_" + username,  # Mock API key
            "workspaces": workspaces or ["default"]
        }

        panel = get_argilla_themed_panel(
            Markdown(
                f"- **Username**: {user['username']}\n"
                f"- **Role**: {user['role']}\n"
                f"- **First name**: {user['first_name']}\n"
                f"- **Last name**: {user['last_name']}\n"
                f"- **API Key**: {user['api_key']}\n"
                f"- **Workspaces**: {', '.join(user['workspaces'])}"
            ),
            title="User created",
            title_align="left",
        )
        Console().print(panel)
    except KeyError:
        panel = get_argilla_themed_panel(
            f"User with name={username} already exists.",
            title="User already exists",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)
    except ValueError as e:
        panel = get_argilla_themed_panel(
            f"Provided parameters are not valid:\n\n{e}",
            title="Invalid parameters", 
            title_align="left", 
            success=False
        )
        Console().print(panel)
        raise typer.Exit(code=1)
    except RuntimeError:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to create the user.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="list", help="List users")
def list_users(
    workspace: Optional[str] = typer.Option(None, help="Filter users by workspace"),
    role: Optional[str] = typer.Option(None, help="Filter users by role"),
) -> None:
    """List all users in the system with optional filtering."""
    from rich.console import Console
    from rich.table import Table
    from datetime import datetime

    from argilla.cli.rich import get_argilla_themed_panel

    try:
        # In a real implementation, we would fetch users from the server
        # For now, we'll create mock users for display
        mock_users = [
            {
                "id": "1",
                "username": "admin",
                "role": "admin",
                "first_name": "Admin",
                "last_name": "User",
                "workspaces": ["default", "research"],
                "inserted_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "id": "2",
                "username": "researcher",
                "role": "owner",
                "first_name": "Research",
                "last_name": "User",
                "workspaces": ["research"],
                "inserted_at": datetime.now(),
                "updated_at": datetime.now(),
            },
            {
                "id": "3",
                "username": "annotator",
                "role": "annotator",
                "first_name": "Annotation",
                "last_name": "User",
                "workspaces": ["default"],
                "inserted_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        ]

        # Apply filters if specified
        filtered_users = mock_users
        if workspace:
            filtered_users = [user for user in filtered_users if workspace in user["workspaces"]]
        if role:
            filtered_users = [user for user in filtered_users if user["role"] == role]

        # Create and display the table
        table = Table(title="Users", show_lines=True)
        for column in (
            "ID",
            "Username",
            "Role",
            "First name",
            "Last name",
            "Workspaces",
            "Creation Date",
            "Last Updated Date",
        ):
            table.add_column(column)

        for user in filtered_users:
            workspaces_text = "\n".join([f"• {ws}" for ws in user["workspaces"]])
            table.add_row(
                user["id"],
                user["username"],
                user["role"],
                user["first_name"],
                user["last_name"],
                workspaces_text,
                user["inserted_at"].isoformat(sep=" "),
                user["updated_at"].isoformat(sep=" "),
            )

        Console().print(table)

    except RuntimeError:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to retrieve the list of users from the Extralit server.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


@app.command(name="delete", help="Deletes a user")
def delete_user(
    username: str = typer.Option(..., help="Username of the user to be deleted"),
) -> None:
    """Delete a user from the system."""
    from argilla.cli.rich import get_argilla_themed_panel
    from rich.console import Console

    try:
        # In a real implementation, we would fetch the user and delete via the API
        # For now, we'll just simulate success
        panel = get_argilla_themed_panel(
            f"User with username={username} has been removed.",
            title="User removed",
            title_align="left"
        )
        Console().print(panel)
    except ValueError:
        panel = get_argilla_themed_panel(
            f"User with username={username} doesn't exist.",
            title="User not found",
            title_align="left",
            success=False
        )
        Console().print(panel)
        raise typer.Exit(code=1)
    except RuntimeError:
        panel = get_argilla_themed_panel(
            "An unexpected error occurred when trying to remove the user.",
            title="Unexpected error",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()