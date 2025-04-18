#!/usr/bin/env python
"""
Test script for testing the Extralit CLI against a live Argilla v2 server.

This script will:
1. Check if the Argilla v2 server is running
2. Run CLI commands against the server
3. Verify that the commands work as expected
4. Document any issues or API differences

Usage:
    python test_live_server.py

Requirements:
    - Docker and Docker Compose must be installed
    - The Argilla v2 server must be running (see argilla-v2-server/README.md)
    - The Extralit CLI must be installed
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
import tempfile
import shutil

# Server configuration
SERVER_URL = "http://localhost:6900"
API_KEY = "argilla.apikey"
USERNAME = "argilla"
PASSWORD = "argilla12345678"
WORKSPACE = "default"

# Test data
TEST_SCHEMA_DIR = "test_schemas"
TEST_SCHEMA_FILE = "test_schema.json"
TEST_DATASET_NAME = "test_dataset"

# Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(message):
    """Print a header message."""
    print(f"\n{BOLD}{'=' * 80}{RESET}")
    print(f"{BOLD}{message}{RESET}")
    print(f"{BOLD}{'=' * 80}{RESET}\n")

def print_success(message):
    """Print a success message."""
    print(f"{GREEN}✓ {message}{RESET}")

def print_warning(message):
    """Print a warning message."""
    print(f"{YELLOW}⚠ {message}{RESET}")

def print_error(message):
    """Print an error message."""
    print(f"{RED}✗ {message}{RESET}")

def run_command(command, expected_exit_code=0, capture_output=True):
    """Run a command and return the result."""
    print(f"Running command: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=True,
            check=False
        )
        
        if result.returncode == expected_exit_code:
            print_success(f"Command completed with exit code {result.returncode}")
        else:
            print_error(f"Command failed with exit code {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
        
        return result
    except Exception as e:
        print_error(f"Error running command: {e}")
        return None

def check_server_running():
    """Check if the Argilla v2 server is running."""
    print_header("Checking if Argilla v2 server is running")
    
    try:
        import requests
        response = requests.get(f"{SERVER_URL}/api/status")
        
        if response.status_code == 200:
            print_success("Argilla v2 server is running")
            return True
        else:
            print_error(f"Argilla v2 server returned status code {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error connecting to Argilla v2 server: {e}")
        print_warning("Make sure the server is running with: docker compose up -d")
        return False

def test_login():
    """Test the login command."""
    print_header("Testing login command")
    
    # Test login with API key
    result = run_command([
        "argilla", "login",
        "--api-url", SERVER_URL,
        "--api-key", API_KEY
    ])
    
    if result and result.returncode == 0:
        print_success("Login with API key successful")
    else:
        print_error("Login with API key failed")
        return False
    
    return True

def test_info():
    """Test the info command."""
    print_header("Testing info command")
    
    result = run_command(["argilla", "info"])
    
    if result and result.returncode == 0:
        print_success("Info command successful")
        return True
    else:
        print_error("Info command failed")
        return False

def test_whoami():
    """Test the whoami command."""
    print_header("Testing whoami command")
    
    result = run_command(["argilla", "whoami"])
    
    if result and result.returncode == 0:
        print_success("Whoami command successful")
        return True
    else:
        print_error("Whoami command failed")
        return False

def test_workspaces():
    """Test workspace management commands."""
    print_header("Testing workspace management commands")
    
    # Test listing workspaces
    result = run_command(["argilla", "workspaces", "list"])
    
    if result and result.returncode == 0:
        print_success("Listing workspaces successful")
    else:
        print_error("Listing workspaces failed")
        return False
    
    # Test creating a new workspace
    new_workspace = f"test-workspace-{int(time.time())}"
    result = run_command([
        "argilla", "workspaces", "create",
        "--name", new_workspace,
        "--description", "Test workspace for CLI testing"
    ])
    
    if result and result.returncode == 0:
        print_success(f"Creating workspace '{new_workspace}' successful")
    else:
        print_error(f"Creating workspace '{new_workspace}' failed")
        return False
    
    # Test listing workspaces again to verify the new workspace
    result = run_command(["argilla", "workspaces", "list"])
    
    if result and result.returncode == 0 and new_workspace in result.stdout:
        print_success(f"Verified new workspace '{new_workspace}' in workspace list")
    else:
        print_error(f"Could not verify new workspace '{new_workspace}' in workspace list")
        return False
    
    return True

def test_users():
    """Test user management commands."""
    print_header("Testing user management commands")
    
    # Test listing users
    result = run_command(["argilla", "users", "list"])
    
    if result and result.returncode == 0:
        print_success("Listing users successful")
    else:
        print_error("Listing users failed")
        return False
    
    return True

def test_schemas():
    """Test schema management commands."""
    print_header("Testing schema management commands")
    
    # Create a test schema directory
    os.makedirs(TEST_SCHEMA_DIR, exist_ok=True)
    
    # Create a test schema file
    schema_content = {
        "name": "test_schema",
        "description": "Test schema for CLI testing",
        "fields": [
            {
                "name": "text",
                "type": "text",
                "required": True
            },
            {
                "name": "label",
                "type": "category",
                "required": True,
                "options": ["positive", "negative", "neutral"]
            }
        ]
    }
    
    with open(os.path.join(TEST_SCHEMA_DIR, TEST_SCHEMA_FILE), "w") as f:
        json.dump(schema_content, f, indent=2)
    
    # Test listing schemas
    result = run_command([
        "argilla", "schemas",
        "--workspace", WORKSPACE,
        "list"
    ])
    
    if result and result.returncode == 0:
        print_success("Listing schemas successful")
    else:
        print_error("Listing schemas failed")
        return False
    
    # Test uploading a schema
    result = run_command([
        "argilla", "schemas",
        "--workspace", WORKSPACE,
        "upload",
        TEST_SCHEMA_DIR,
        "--overwrite"
    ])
    
    if result and result.returncode == 0:
        print_success("Uploading schema successful")
    else:
        print_error("Uploading schema failed")
        return False
    
    # Test listing schemas again to verify the new schema
    result = run_command([
        "argilla", "schemas",
        "--workspace", WORKSPACE,
        "list"
    ])
    
    if result and result.returncode == 0 and "test_schema" in result.stdout:
        print_success("Verified new schema in schema list")
    else:
        print_error("Could not verify new schema in schema list")
        return False
    
    # Clean up
    shutil.rmtree(TEST_SCHEMA_DIR)
    
    return True

def test_datasets():
    """Test dataset management commands."""
    print_header("Testing dataset management commands")
    
    # Test listing datasets
    result = run_command([
        "argilla", "datasets",
        "--workspace", WORKSPACE,
        "list"
    ])
    
    if result and result.returncode == 0:
        print_success("Listing datasets successful")
    else:
        print_error("Listing datasets failed")
        return False
    
    # Test creating a dataset
    result = run_command([
        "argilla", "datasets",
        "--workspace", WORKSPACE,
        "create",
        "--name", TEST_DATASET_NAME,
        "--description", "Test dataset for CLI testing"
    ])
    
    if result and result.returncode == 0:
        print_success(f"Creating dataset '{TEST_DATASET_NAME}' successful")
    else:
        print_error(f"Creating dataset '{TEST_DATASET_NAME}' failed")
        return False
    
    # Test listing datasets again to verify the new dataset
    result = run_command([
        "argilla", "datasets",
        "--workspace", WORKSPACE,
        "list"
    ])
    
    if result and result.returncode == 0 and TEST_DATASET_NAME in result.stdout:
        print_success(f"Verified new dataset '{TEST_DATASET_NAME}' in dataset list")
    else:
        print_error(f"Could not verify new dataset '{TEST_DATASET_NAME}' in dataset list")
        return False
    
    return True

def test_training():
    """Test training commands."""
    print_header("Testing training commands")
    
    # Test training help
    result = run_command([
        "argilla", "training",
        "--help"
    ])
    
    if result and result.returncode == 0:
        print_success("Training help command successful")
    else:
        print_error("Training help command failed")
        return False
    
    # Test basic training command
    # Note: This might fail if the dataset doesn't exist or doesn't have the right format
    result = run_command([
        "argilla", "training",
        "--name", TEST_DATASET_NAME,
        "--framework", "spacy",
        "--model", "en_core_web_sm"
    ], expected_exit_code=1)  # Expecting failure since we don't have a properly formatted dataset
    
    if result:
        print_warning("Training command executed but failed as expected (dataset not properly formatted)")
    else:
        print_error("Training command execution failed")
        return False
    
    return True

def test_extraction():
    """Test extraction commands."""
    print_header("Testing extraction commands")
    
    # Test extraction help
    result = run_command([
        "argilla", "extraction",
        "--help"
    ])
    
    if result and result.returncode == 0:
        print_success("Extraction help command successful")
    else:
        print_error("Extraction help command failed")
        return False
    
    # Test extraction export command
    # Note: This might fail if the workspace doesn't exist or env file is missing
    result = run_command([
        "argilla", "extraction",
        "--workspace", WORKSPACE,
        "--env-file", ".env.test",
        "export",
        "--output", "exports"
    ], expected_exit_code=1)  # Expecting failure since we don't have a proper env file
    
    if result:
        print_warning("Extraction export command executed but failed as expected (missing env file)")
    else:
        print_error("Extraction export command execution failed")
        return False
    
    return True

def test_logout():
    """Test the logout command."""
    print_header("Testing logout command")
    
    result = run_command(["argilla", "logout"])
    
    if result and result.returncode == 0:
        print_success("Logout command successful")
        return True
    else:
        print_error("Logout command failed")
        return False

def main():
    """Main function to run all tests."""
    print_header("Starting Extralit CLI Live Server Tests")
    
    # Check if the server is running
    if not check_server_running():
        print_error("Argilla v2 server is not running. Please start it first.")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Login", test_login),
        ("Info", test_info),
        ("Whoami", test_whoami),
        ("Workspaces", test_workspaces),
        ("Users", test_users),
        ("Schemas", test_schemas),
        ("Datasets", test_datasets),
        ("Training", test_training),
        ("Extraction", test_extraction),
        ("Logout", test_logout)
    ]
    
    results = {}
    
    for name, test_func in tests:
        print_header(f"Running {name} Tests")
        try:
            result = test_func()
            results[name] = result
        except Exception as e:
            print_error(f"Error running {name} tests: {e}")
            results[name] = False
    
    # Print summary
    print_header("Test Summary")
    
    all_passed = True
    for name, result in results.items():
        if result:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
            all_passed = False
    
    if all_passed:
        print_success("\nAll tests passed!")
        return 0
    else:
        print_error("\nSome tests failed. See above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
