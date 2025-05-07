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

from typing import Optional, Union
import traceback

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text


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