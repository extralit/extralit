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

from argilla.cli.app import app


@pytest.fixture
def runner():
    """Fixture providing a CLI runner."""
    return CliRunner()


def test_workspaces_help(runner):
    """Test that the workspaces command shows help message."""
    result = runner.invoke(app, ["workspaces", "--help"])
    assert result.exit_code == 0
    assert "Commands for workspace management" in result.stdout


def test_workspaces_list_command_help(runner):
    """Test the help message for the 'list' subcommand."""
    result = runner.invoke(app, ["workspaces", "list", "--help"])
    assert result.exit_code == 0
    assert "List workspaces" in result.stdout


def test_workspaces_create_command_help(runner):
    """Test the help message for the 'create' subcommand."""
    result = runner.invoke(app, ["workspaces", "create", "--help"])
    assert result.exit_code == 0
    assert "Creates a new workspace" in result.stdout


def test_workspaces_add_user_command_help(runner):
    """Test the help message for the 'add-user' subcommand."""
    result = runner.invoke(app, ["workspaces", "add-user", "--help"])
    assert result.exit_code == 0
    assert "Add a user to a workspace" in result.stdout


def test_workspaces_delete_user_command_help(runner):
    """Test the help message for the 'delete-user' subcommand."""
    result = runner.invoke(app, ["workspaces", "delete-user", "--help"])
    assert result.exit_code == 0
    assert "Remove a user from a workspace" in result.stdout


@patch("argilla.cli.workspaces.__main__.get_workspaces")
def test_workspaces_list(mock_get_workspaces, runner):
    """Test the 'list' command functionality."""
    # Mock the get_workspaces function to return test data
    mock_get_workspaces.return_value = [
        {
            "id": "1",
            "name": "default",
            "created_at": "2025-04-10 10:00:00",
            "updated_at": "2025-04-10 10:00:00"
        },
        {
            "id": "2",
            "name": "research",
            "created_at": "2025-04-12 15:30:45",
            "updated_at": "2025-04-12 15:30:45"
        }
    ]
    
    result = runner.invoke(app, ["workspaces", "list"])
    assert result.exit_code == 0
    assert "default" in result.stdout
    assert "research" in result.stdout
    mock_get_workspaces.assert_called_once()


@patch("argilla.cli.workspaces.__main__.create_workspace")
@patch("typer.prompt")
def test_workspaces_create(mock_prompt, mock_create_workspace, runner):
    """Test the 'create' command functionality."""
    # Mock the prompt to return a workspace name
    mock_prompt.return_value = "test-workspace"
    
    # Mock the create_workspace function
    mock_create_workspace.return_value = {
        "id": "3",
        "name": "test-workspace",
        "created_at": "2025-04-14 12:00:00",
        "updated_at": "2025-04-14 12:00:00"
    }
    
    result = runner.invoke(app, ["workspaces", "create"])
    assert result.exit_code == 0
    assert "Workspace created" in result.stdout
    assert "test-workspace" in result.stdout
    mock_create_workspace.assert_called_once_with("test-workspace")


@patch("argilla.cli.workspaces.__main__.add_user_to_workspace")
def test_workspaces_add_user(mock_add_user, runner):
    """Test the 'add-user' command functionality."""
    # Mock the add_user_to_workspace function
    mock_add_user.return_value = True
    
    result = runner.invoke(app, [
        "workspaces", "add-user",
        "--name", "research",
        "--username", "testuser",
        "--role", "admin"
    ])
    
    assert result.exit_code == 0
    assert "User added" in result.stdout
    assert "testuser" in result.stdout
    assert "research" in result.stdout
    mock_add_user.assert_called_once()


@patch("argilla.cli.workspaces.__main__.delete_user_from_workspace")
def test_workspaces_delete_user(mock_delete_user, runner):
    """Test the 'delete-user' command functionality."""
    # Mock the delete_user_from_workspace function
    mock_delete_user.return_value = True
    
    result = runner.invoke(app, [
        "workspaces", "delete-user",
        "--name", "research",
        "--username", "testuser"
    ])
    
    assert result.exit_code == 0
    assert "User removed" in result.stdout
    assert "testuser" in result.stdout
    assert "research" in result.stdout
    mock_delete_user.assert_called_once()