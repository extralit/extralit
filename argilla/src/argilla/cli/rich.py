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

from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text


def get_argilla_themed_panel(
    renderable: RenderableType,
    title: Optional[Union[str, Text]] = None,
    title_align: str = "center",
    success: bool = True,
) -> Panel:
    """
    Returns a rich panel with Argilla theme.

    Args:
        renderable: The content to display
        title: The title of the panel
        title_align: The alignment of the title
        success: If True, use success style; if False, use error style

    Returns:
        A rich panel with Argilla theme
    """
    return Panel(
        renderable=renderable,
        title=title,
        title_align=title_align,
        border_style="green" if success else "red",
        padding=1,
    )