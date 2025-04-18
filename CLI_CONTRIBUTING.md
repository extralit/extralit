# Contributing to Extralit CLI

Thank you for your interest in contributing to the Extralit CLI! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.9 or later
- Git

### Setting Up the Development Environment

1. Clone the repository:

```bash
git clone https://github.com/extralit/extralit.git
cd extralit
```

2. Install the package in development mode:

```bash
pip install -e ".[dev]"
```

3. Install pre-commit hooks:

```bash
pre-commit install
```

## Project Structure

The CLI code is located in the `argilla/src/argilla/cli` directory:

- `app.py`: The main entry point for the CLI
- `typer_ext.py`: Extensions to the Typer library
- `callback.py`: Common callback functions
- `rich.py`: Utilities for rich terminal output
- Command modules:
  - `datasets/`: Dataset management commands
  - `extraction/`: Extraction pipeline commands
  - `info/`: Server information commands
  - `login/`: Authentication commands
  - `logout/`: Logout functionality
  - `schemas/`: Schema management commands
  - `training/`: Model training commands
  - `users/`: User management commands
  - `whoami/`: User identification commands
  - `workspaces/`: Workspace management commands

## Adding a New Command

1. Create a new module in the appropriate directory
2. Define your command using Typer
3. Register your command in `app.py`
4. Add tests for your command in `tests/unit/cli/`

Example:

```python
# src/argilla/cli/mycommand/__main__.py
import typer
from argilla.cli.callback import init_callback
from argilla.cli.rich import get_argilla_themed_panel
from rich.console import Console

app = typer.Typer(help="My command help text", no_args_is_help=True)

@app.callback()
def callback(ctx: typer.Context):
    """Callback for my command."""
    init_callback()

@app.command(name="subcommand", help="My subcommand help text")
def my_subcommand(
    param: str = typer.Argument(..., help="Parameter help text"),
):
    """My subcommand docstring."""
    # Command implementation
    panel = get_argilla_themed_panel(
        f"Executed my subcommand with parameter: {param}",
        title="Success",
        title_align="left",
    )
    Console().print(panel)
```

Then register your command in `app.py`:

```python
from argilla.cli import mycommand
app.add_typer(mycommand.app, name="mycommand")
```

## Testing

### Running Tests

Run the tests with pytest:

```bash
python -m pytest tests/unit/cli/
```

### Writing Tests

Add tests for your command in `tests/unit/cli/`:

```python
# tests/unit/cli/test_mycommand.py
import pytest
from typer.testing import CliRunner
from unittest.mock import patch

from argilla.cli.app import app

@pytest.fixture
def runner():
    """Fixture providing a CLI runner."""
    return CliRunner()

def test_mycommand_help(runner):
    """Test that the mycommand shows help message."""
    result = runner.invoke(app, ["mycommand", "--help"])
    assert result.exit_code == 0
    assert "my command help text" in result.stdout.lower()

@patch("rich.console.Console.print")
def test_mycommand_subcommand(mock_print, runner):
    """Test the subcommand functionality."""
    result = runner.invoke(app, ["mycommand", "subcommand", "test-param"])
    assert result.exit_code == 0
    mock_print.assert_called_once()
```

## Code Style

We use the following tools for code style:

- Black for code formatting
- Ruff for linting
- isort for import sorting

You can run these tools with:

```bash
# Format code
black .

# Lint code
ruff check .

# Sort imports
isort .
```

## Documentation

When adding a new command, make sure to:

1. Add docstrings to all functions and classes
2. Update the CLI README.md with usage examples
3. Add the command to the documentation

## Pull Request Process

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Run the tests to ensure they pass
5. Submit a pull request

## Live Server Testing

For testing against a live Argilla v2 server, you can use the `test_live_server.py` script:

```bash
python test_live_server.py
```

This script will:
1. Check if the Argilla v2 server is running
2. Run CLI commands against the server
3. Verify that the commands work as expected
4. Document any issues or API differences

Make sure you have a local Argilla v2 server running before running this script. See `argilla-v2-server/README.md` for instructions on setting up a local server.
