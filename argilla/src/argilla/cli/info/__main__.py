# Copyright 2024-present, Extralit Labs, Inc.
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

import typer

from argilla.cli.callback import init_callback
from argilla.cli.rich import get_argilla_themed_panel
from rich.console import Console
from rich.markdown import Markdown

app = typer.Typer(invoke_without_command=True)


def get_server_info():
    """Get server information.

    Returns:
        ServerInfo: Object containing server information.
    """
    # Initialize client and get server info
    client = init_callback()

    # Get server info from client
    server_info = client.get_server_info()

    # Create ServerInfo object for backward compatibility
    class ServerInfo:
        def __init__(self):
            self.url = server_info["url"]
            self.version = server_info["version"]
            self.database_version = server_info["database_version"]

    return ServerInfo()


@app.callback(help="Displays information about the Extralit client and server")
def info() -> None:
    """Display information about the Extralit client and server."""
    try:
        from argilla import __version__ as version
    except ImportError:
        version = "2.0.0"  # Fallback version for development

    # Get server info (this will initialize the client)
    info = get_server_info()

    panel = get_argilla_themed_panel(
        Markdown(
            f"Connected to {info.url}\n"
            f"- **Client version:** {version}\n"
            f"- **Server version:** {info.version}\n"
            f"- **Database version:** {info.database_version}\n"
        ),
        title="Extralit Info",
        title_align="left",
    )

    Console().print(panel)


if __name__ == "__main__":
    app()
