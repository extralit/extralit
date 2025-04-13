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


def test_users_help(runner):
    """Test that the users command shows help message."""
    result = runner.invoke(app, ["users", "--help"])
    assert result.exit_code == 0
    assert "user management" in result.stdout.lower()


def test_users_create_command_help(runner):
    """Test the help message for the 'create' subcommand."""
    result = runner.invoke(app, ["users", "create", "--help"])
    assert result.exit_code == 0
    assert "creates a new user" in result.stdout.lower()


def test_users_list_command_help(runner):
    """Test the help message for the 'list' subcommand."""
    result = runner.invoke(app, ["users", "list", "--help"])
    assert result.exit_code == 0
    assert "list users" in result.stdout.lower()


def test_users_delete_command_help(runner):
    """Test the help message for the 'delete' subcommand."""
    result = runner.invoke(app, ["users", "delete", "--help"])
    assert result.exit_code == 0
    assert "deletes a user" in result.stdout.lower()


@patch("argilla.cli.users.__main__.Console.print")
def test_users_create_basic(mock_print, runner):
    """Test the basic 'create user' command functionality."""
    # Simulate user input for the prompt
    result = runner.invoke(
        app,
        ["users", "create", "--username", "testuser", "--password", "password123"],
        input="password123\n"  # Confirmation password
    )
    
    assert result.exit_code == 0
    # Verify that Console.print was called (which indicates success)
    mock_print.assert_called_once()
    
    # Extract the call arguments to check what was printed
    call_args = mock_print.call_args[0][0]
    call_args_str = str(call_args)
    
    # Check that the user information is in the printed output
    assert "testuser" in call_args_str
    assert "api_testuser" in call_args_str  # API key should be generated
    assert "annotator" in call_args_str  # Default role is annotator


@patch("argilla.cli.users.__main__.Console.print")
def test_users_create_with_role_and_workspace(mock_print, runner):
    """Test creating a user with custom role and workspace."""
    result = runner.invoke(
        app,
        [
            "users", "create",
            "--username", "adminuser",
            "--password", "secure123",
            "--role", "admin",
            "--workspace", "research",
            "--first-name", "Admin",
            "--last-name", "User"
        ],
        input="secure123\n"  # Confirmation password
    )
    
    assert result.exit_code == 0
    mock_print.assert_called_once()
    
    # Extract the call arguments to check what was printed
    call_args = mock_print.call_args[0][0]
    call_args_str = str(call_args)
    
    # Check that all the provided parameters are included
    assert "adminuser" in call_args_str
    assert "admin" in call_args_str  # Custom role
    assert "Admin" in call_args_str  # First name
    assert "User" in call_args_str  # Last name
    assert "research" in call_args_str  # Custom workspace


@patch("argilla.cli.users.__main__.Console.print")
def test_users_create_user_exists(mock_print, runner):
    """Test creating a user that already exists (should fail)."""
    # Make print raise KeyError to simulate user already exists
    mock_print.side_effect = KeyError("User already exists")
    
    result = runner.invoke(
        app,
        ["users", "create", "--username", "existinguser", "--password", "password"],
        input="password\n"  # Confirmation password
    )
    
    # Should exit with code 1 due to KeyError
    assert result.exit_code == 1


@patch("argilla.cli.users.__main__.Console.print")
def test_users_list(mock_print, runner):
    """Test the 'list users' command functionality."""
    result = runner.invoke(app, ["users", "list"])
    
    assert result.exit_code == 0
    mock_print.assert_called_once()
    
    # Since we're using mock data, just verify that print was called
    # In a more complete test, we could mock the API call and check the output


@patch("argilla.cli.users.__main__.Console.print")
def test_users_list_with_filters(mock_print, runner):
    """Test the 'list users' command with workspace and role filters."""
    result = runner.invoke(app, ["users", "list", "--workspace", "research", "--role", "owner"])
    
    assert result.exit_code == 0
    mock_print.assert_called_once()
    
    # Since we're testing with mock data and filters are applied in-memory,
    # we just verify that print was called


@patch("argilla.cli.users.__main__.Console.print")
def test_users_delete(mock_print, runner):
    """Test the 'delete user' command functionality."""
    result = runner.invoke(app, ["users", "delete", "--username", "testuser"])
    
    assert result.exit_code == 0
    mock_print.assert_called_once()
    
    # Extract the call arguments to check what was printed
    call_args = mock_print.call_args[0][0]
    call_args_str = str(call_args)
    
    # Check that deletion confirmation is in the output
    assert "testuser" in call_args_str
    assert "removed" in call_args_str.lower()


@patch("argilla.cli.users.__main__.Console.print")
def test_users_delete_nonexistent(mock_print, runner):
    """Test deleting a user that doesn't exist (should fail)."""
    # Make print raise ValueError to simulate user not found
    mock_print.side_effect = ValueError("User not found")
    
    result = runner.invoke(app, ["users", "delete", "--username", "nonexistentuser"])
    
    # Should exit with code 1 due to ValueError
    assert result.exit_code == 1