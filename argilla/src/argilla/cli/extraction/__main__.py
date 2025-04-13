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
from argilla.cli.callback import init_callback

import typer

from argilla.cli.extraction.export import export_data

_COMMANDS_REQUIRING_WORKSPACE = ["export"]
_COMMANDS_REQUIRING_ENVFILE = ["export"]

def callback(
    ctx: typer.Context,
    workspace: str = typer.Option(None, help="Name of the workspace to which apply the command."),
    env_file: str = typer.Option(None, help="Path to .env file with environment variables containing S3 credentials."),
) -> None:
    """Callback for extraction commands.
    
    This is a simplified version that will be fully implemented in Phase 3.
    """
    # Initialize callback for all commands
    init_callback()
    
    # Store workspace and env_file info in context object for commands that need it
    ctx.obj = {
        "workspace": workspace,
        "env_file": env_file,
    }


app = typer.Typer(help="Commands for extraction data management", no_args_is_help=True, callback=callback)

app.command(name="export", help="Export data from extraction datasets")(export_data)

if __name__ == "__main__":
    app()
