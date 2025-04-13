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

import json
from pathlib import Path

import typer
from rich.markdown import Markdown

app = typer.Typer(invoke_without_command=True)


def get_current_user():
    """Get information about the current user."""
    # In a full implementation, this would use the v2 API client
    # For now, we'll read from the credentials file
    cred_file = Path.home() / ".argilla" / "credentials.json"
    
    if not cred_file.exists():
        raise ValueError("Not logged in. Please run 'extralit login' first.")
    
    with open(cred_file, "r") as f:
        credentials = json.load(f)
    
    # In a real implementation, we would fetch user details from the server
    # For now, we'll simulate a user based on the API key and URL
    class User:
        def __init__(self, api_url, api_key):
            self.username = "current-user"  # Placeholder
            self.role = "owner"  # Placeholder
            self.first_name = "Current"  # Placeholder
            self.last_name = "User"  # Placeholder
            self.api_key = api_key[:5] + "..." if api_key else None
            self.workspaces = ["default"]  # Placeholder
            self.api_url = api_url
            
    return User(credentials.get("api_url"), credentials.get("api_key"))


@app.callback(help="Show information about the current user")
def whoami() -> None:
    """Display information about the current user."""
    from argilla.cli.callback import init_callback
    from argilla.cli.rich import get_argilla_themed_panel
    from rich.console import Console

    try:
        init_callback()
        user = get_current_user()
        
        panel = get_argilla_themed_panel(
            Markdown(
                f"- **Username**: {user.username}\n"
                f"- **Role**: {user.role}\n"
                f"- **First name**: {user.first_name}\n"
                f"- **Last name**: {user.last_name}\n"
                f"- **API Key**: {user.api_key}\n"
                f"- **Workspaces**: {', '.join(user.workspaces)}\n"
                f"- **Server URL**: {user.api_url}"
            ),
            title="Current User",
            title_align="left",
        )
        Console().print(panel)
    except ValueError as e:
        from argilla.cli.rich import get_argilla_themed_panel
        panel = get_argilla_themed_panel(
            str(e),
            title="Not logged in",
            title_align="left",
            success=False,
        )
        Console().print(panel)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()