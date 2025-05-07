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

from typing import TYPE_CHECKING, List, Optional, Union
import traceback

from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

if TYPE_CHECKING:
    from argilla._resource import Resource


def get_argilla_themed_panel(
    renderable: RenderableType,
    title: Optional[Union[str, Text]] = None,
    title_align: str = "center",
    success: bool = True,
    exception: Optional[Exception] = None,
    debug: bool = False,
) -> Panel:
    """
    Returns a rich panel with Argilla theme.

    Args:
        renderable: The content to display
        title: The title of the panel
        title_align: The alignment of the title
        success: If True, use success style; if False, use error style
        exception: Optional exception to include in the panel
        debug: If True and exception is provided, include a minimal stack trace

    Returns:
        A rich panel with Argilla theme
    """
    content = renderable

    if exception is not None and debug:
        tb = traceback.extract_tb(exception.__traceback__)
        # Get just the first and last frames for a minimal trace
        if len(tb) > 1:
            minimal_tb = [tb[0], tb[-1]]
        else:
            minimal_tb = tb

        trace_str = "\n\n[bold]Debug trace:[/bold]\n"
        for frame in minimal_tb:
            file, line, func, code = frame
            trace_str += f"File '{file}', line {line}, in {func}\n  {code}\n"

        if isinstance(content, str):
            content = f"{content}{trace_str}"
        else:
            # For other renderables, we wrap both in a list
            content = [content, Text.from_markup(trace_str)]

    return Panel(
        renderable=content,
        title=title,
        title_align=title_align,
        border_style="green" if success else "red",
        padding=1,
    )


def print_rich_table(
    resources: List["Resource"], columns: Optional[List[str]] = None, title: Optional[str] = None
) -> None:
    """
    Prints resources in a rich formatted table.

    Args:
        resources: List of resources to display
        columns: Optional list of columns to display. If None, uses default columns.
        title: Optional title for the table. If None, uses the resource_type.
    """
    resource_type = resources[0].__class__.__name__

    if not resources:
        Console().print(f"No {resource_type.lower()}s found")
        return

    title = title or resource_type + "s"
    table = Table(title=title, show_lines=False)

    column_configs = {
        "Dataset": {
            "columns": ["ID", "Name", "Workspace", "Creation Date", "Last Activity Date"],
            "getters": {
                "ID": lambda r: str(r.id),
                "Name": lambda r: r.name,
                "Workspace": lambda r: r.workspace.name,
                "Creation Date": lambda r: r.inserted_at.isoformat(sep=" "),
                "Last Activity Date": lambda r: r._model.last_activity_at.isoformat(sep=" "),
            },
        },
        "User": {
            "columns": ["ID", "Username", "Role", "Creation Date"],
            "getters": {
                "ID": lambda r: str(r.id),
                "Username": lambda r: r.username,
                "Role": lambda r: r.role,
                "Creation Date": lambda r: r.inserted_at.isoformat(sep=" "),
            },
        },
        "Workspace": {
            "columns": ["ID", "Name", "Creation Date", "Last Update Date"],
            "getters": {
                "ID": lambda r: str(r.id),
                "Name": lambda r: r.name,
                "Creation Date": lambda r: r.inserted_at.isoformat(sep=" "),
                "Last Update Date": lambda r: r.updated_at.isoformat(sep=" "),
            },
        },
    }

    config = column_configs.get(resource_type, {})
    display_columns = columns or config.get("columns", [])
    getters = config.get("getters", {})

    for column in display_columns:
        table.add_column(column, justify="center" if column != "Name" else "left")

    for resource in resources:
        row_values = []
        for column in display_columns:
            getter = getters.get(column)
            if getter:
                try:
                    value = getter(resource)
                except (AttributeError, KeyError):
                    value = "N/A"
            else:
                try:
                    value = getattr(resource, column.lower().replace(" ", "_"), "N/A")
                except AttributeError:
                    value = "N/A"
            row_values.append(str(value))

        table.add_row(*row_values)

    Console().print(table)
