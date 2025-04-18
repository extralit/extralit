#!/usr/bin/env python
"""
Simple test script to verify connection to Argilla V2 server and create a workspace.
"""

import argparse
import sys

import argilla as rg
from argilla.client import Argilla

# Colors for terminal output
GREEN = "\033[92m"
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

def print_error(message):
    """Print an error message."""
    print(f"{RED}✗ {message}{RESET}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test connection to Argilla V2 server.")
    parser.add_argument("--api-url", required=True, help="URL of the Argilla V2 server")
    parser.add_argument("--api-key", required=True, help="API key for authentication")
    args = parser.parse_args()
    
    print_header("Testing Connection to Argilla V2 Server")
    
    # Try different methods to connect to the server
    
    print("Method 1: Using Argilla.from_credentials")
    try:
        client = Argilla.from_credentials(api_url=args.api_url, api_key=args.api_key)
        print_success("Connected to Argilla V2 server using Argilla.from_credentials")
        print(f"Client type: {type(client)}")
        print(f"Client attributes: {dir(client)}")
    except Exception as e:
        print_error(f"Failed to connect using Argilla.from_credentials: {str(e)}")
    
    print("\nMethod 2: Using rg.init")
    try:
        rg.init(api_url=args.api_url, api_key=args.api_key)
        print_success("Connected to Argilla V2 server using rg.init")
    except Exception as e:
        print_error(f"Failed to connect using rg.init: {str(e)}")
    
    print("\nMethod 3: Using rg.Argilla.from_credentials")
    try:
        client = rg.Argilla.from_credentials(api_url=args.api_url, api_key=args.api_key)
        print_success("Connected to Argilla V2 server using rg.Argilla.from_credentials")
        print(f"Client type: {type(client)}")
        print(f"Client attributes: {dir(client)}")
    except Exception as e:
        print_error(f"Failed to connect using rg.Argilla.from_credentials: {str(e)}")
    
    print_header("Testing Workspace Creation")
    
    print("Method 1: Using rg.Workspace")
    try:
        workspace = rg.Workspace(name="test-workspace-1")
        print_success(f"Created workspace using rg.Workspace: {workspace.name} (ID: {workspace.id})")
        print(f"Workspace type: {type(workspace)}")
        print(f"Workspace attributes: {dir(workspace)}")
    except Exception as e:
        print_error(f"Failed to create workspace using rg.Workspace: {str(e)}")
    
    print("\nMethod 2: Using client.workspaces.create")
    try:
        client = Argilla.from_credentials(api_url=args.api_url, api_key=args.api_key)
        if hasattr(client, 'workspaces'):
            workspace = client.workspaces.create(name="test-workspace-2")
            print_success(f"Created workspace using client.workspaces.create: {workspace.name} (ID: {workspace.id})")
        else:
            print_error("Client does not have 'workspaces' attribute")
    except Exception as e:
        print_error(f"Failed to create workspace using client.workspaces.create: {str(e)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
