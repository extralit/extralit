"""
Test script for testing CLI commands with a local Argilla v2 server.
This script will help us test our CLI commands with the local server.
"""

import os
import sys
import subprocess
from argilla.client.login import ArgillaCredentials

# Server configuration
SERVER_URL = "http://localhost:6900"
API_KEY = "argilla.apikey"
USERNAME = "argilla"
PASSWORD = "argilla12345678"
WORKSPACE = "default"

def run_command(command):
    """Run a CLI command and print the output."""
    print(f"\n=== Running command: {command} ===")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(f"Exit code: {result.returncode}")
    print("Output:")
    print(result.stdout)
    if result.stderr:
        print("Error:")
        print(result.stderr)
    return result

def test_login():
    """Test the login command."""
    # First, make sure we're logged out
    run_command("python -m argilla.cli.app logout")
    
    # Test login with API key
    result = run_command(f"python -m argilla.cli.app login --api-url {SERVER_URL} --api-key {API_KEY}")
    
    # Check if login was successful
    if "Logged in successfully" in result.stdout:
        print("✅ Login test passed")
    else:
        print("❌ Login test failed")

def test_info():
    """Test the info command."""
    result = run_command("python -m argilla.cli.app info")
    
    # Check if info command returned server information
    if "Connected to" in result.stdout and "Server version" in result.stdout:
        print("✅ Info test passed")
    else:
        print("❌ Info test failed")

def test_whoami():
    """Test the whoami command."""
    result = run_command("python -m argilla.cli.app whoami")
    
    # Check if whoami command returned user information
    if "Username" in result.stdout and "Role" in result.stdout:
        print("✅ Whoami test passed")
    else:
        print("❌ Whoami test failed")

def test_workspaces_list():
    """Test the workspaces list command."""
    result = run_command("python -m argilla.cli.app workspaces list")
    
    # Check if workspaces list command returned workspace information
    if "Workspaces" in result.stdout:
        print("✅ Workspaces list test passed")
    else:
        print("❌ Workspaces list test failed")

def test_datasets_list():
    """Test the datasets list command."""
    result = run_command(f"python -m argilla.cli.app datasets list --workspace {WORKSPACE}")
    
    # Check if datasets list command returned dataset information
    if "Datasets" in result.stdout:
        print("✅ Datasets list test passed")
    else:
        print("❌ Datasets list test failed")

def test_datasets_create():
    """Test the datasets create command."""
    # Create a test dataset
    dataset_name = "test-dataset-cli"
    result = run_command(f"python -m argilla.cli.app datasets create --name {dataset_name} --workspace {WORKSPACE}")
    
    # Check if dataset was created successfully
    if "Dataset created successfully" in result.stdout or "Dataset already exists" in result.stdout:
        print("✅ Datasets create test passed")
    else:
        print("❌ Datasets create test failed")

def test_schemas_list():
    """Test the schemas list command."""
    result = run_command(f"python -m argilla.cli.app schemas list --workspace {WORKSPACE}")
    
    # Check if schemas list command returned schema information
    if "Schemas" in result.stdout:
        print("✅ Schemas list test passed")
    else:
        print("❌ Schemas list test failed")

def main():
    """Run all tests."""
    print("=== Testing CLI commands with local Argilla v2 server ===")
    
    # Make sure we're logged in
    test_login()
    
    # Test basic commands
    test_info()
    test_whoami()
    
    # Test workspace commands
    test_workspaces_list()
    
    # Test dataset commands
    test_datasets_list()
    test_datasets_create()
    
    # Test schema commands
    test_schemas_list()
    
    print("\n=== Test summary ===")
    print("All tests completed. Check the results above for any failures.")

if __name__ == "__main__":
    main()
