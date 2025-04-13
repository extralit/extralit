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

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from datetime import datetime

from argilla.cli.app import app


@pytest.fixture
def runner():
    """Fixture providing a CLI runner."""
    return CliRunner()


def test_extraction_help(runner):
    """Test that the extraction command shows help message."""
    result = runner.invoke(app, ["extraction", "--help"])
    assert result.exit_code == 0
    assert "extraction data management" in result.stdout.lower()


def test_extraction_export_command_help(runner):
    """Test the help message for the 'export' subcommand."""
    result = runner.invoke(app, ["extraction", "export", "--help"])
    assert result.exit_code == 0
    assert "export" in result.stdout.lower()


@patch("rich.console.Console.print")
def test_extraction_export_basic(mock_print, runner):
    """Test basic extraction export command functionality."""
    result = runner.invoke(app, [
        "extraction",
        "--workspace", "research",
        "--env-file", ".env.test",
        "export",
        "--dataset", "test_dataset",
        "--output-dir", "exports"
    ])

    assert result.exit_code == 0
    mock_print.assert_called()

    # Extract the call arguments to check what was printed
    call_args = mock_print.call_args[0][0]
    call_args_str = str(call_args)

    # Check that export information is in the output
    assert "test_dataset" in call_args_str
    assert "exports" in call_args_str


@patch("rich.console.Console.print")
def test_extraction_export_with_format(mock_print, runner):
    """Test extraction export command with format option."""
    result = runner.invoke(app, [
        "extraction",
        "--workspace", "research",
        "--env-file", ".env.test",
        "export",
        "--dataset", "test_dataset",
        "--output-dir", "exports",
        "--format", "csv"
    ])

    assert result.exit_code == 0
    mock_print.assert_called()

    # Extract the call arguments to check what was printed
    call_args = mock_print.call_args[0][0]
    call_args_str = str(call_args)

    # Check that format information is in the output
    assert "test_dataset" in call_args_str
    assert "exports" in call_args_str
    assert "csv" in call_args_str


@patch("rich.console.Console.print")
def test_extraction_export_with_filters(mock_print, runner):
    """Test extraction export command with filters."""
    result = runner.invoke(app, [
        "extraction",
        "--workspace", "research",
        "--env-file", ".env.test",
        "export",
        "--dataset", "test_dataset",
        "--output-dir", "exports",
        "--filter", "status=complete",
        "--filter", "type=text"
    ])

    assert result.exit_code == 0
    mock_print.assert_called()

    # Extract the call arguments to check what was printed
    call_args = mock_print.call_args[0][0]
    call_args_str = str(call_args)

    # Check that filter information is in the output
    assert "test_dataset" in call_args_str
    assert "exports" in call_args_str
    assert "status=complete" in call_args_str
    assert "type=text" in call_args_str


@patch("rich.console.Console.print")
def test_extraction_export_missing_workspace(mock_print, runner):
    """Test extraction export command without workspace (should fail)."""
    result = runner.invoke(app, [
        "extraction",
        "export",
        "--dataset", "test_dataset",
        "--output-dir", "exports"
    ])

    # Should exit with non-zero code due to missing workspace
    assert result.exit_code != 0
    assert "workspace" in result.stdout.lower()


@patch("rich.console.Console.print")
def test_extraction_export_missing_env_file(mock_print, runner):
    """Test extraction export command without env file (should fail)."""
    result = runner.invoke(app, [
        "extraction",
        "--workspace", "research",
        "export",
        "--dataset", "test_dataset",
        "--output-dir", "exports"
    ])

    # Should exit with non-zero code due to missing env file
    assert result.exit_code != 0
    assert "env" in result.stdout.lower()


@patch("rich.console.Console.print")
def test_extraction_export_nonexistent_dataset(mock_print, runner):
    """Test exporting a nonexistent dataset (should fail)."""
    # Make print raise ValueError to simulate dataset not found
    mock_print.side_effect = ValueError("Dataset not found")

    result = runner.invoke(app, [
        "extraction",
        "--workspace", "research",
        "--env-file", ".env.test",
        "export",
        "--dataset", "nonexistent_dataset",
        "--output-dir", "exports"
    ])

    # Should exit with code 1 due to ValueError
    assert result.exit_code == 1
