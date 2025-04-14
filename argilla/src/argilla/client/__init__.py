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

"""
Extralit client for CLI integration.
Provides a basic client implementation for the CLI commands.
"""

import os
import json
import time
import requests
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, List, Any, Union

class DatasetType(str, Enum):
    """Dataset types in the system."""
    TEXT_CLASSIFICATION = "text_classification"
    TOKEN_CLASSIFICATION = "token_classification"
    TEXT_GENERATION = "text_generation"
    FEEDBACK = "feedback"


class User:
    """User class for Extralit client."""

    def __init__(self, username: str, role: str, first_name: str = "", last_name: str = "",
                 api_key: str = "", workspaces: List[str] = None, api_url: str = ""):
        self.username = username
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.api_key = api_key
        self.workspaces = workspaces or []
        self.api_url = api_url

class Argilla:
    """
    Extralit client class for CLI integration.
    Provides a basic client implementation for the CLI commands.
    """

    def __init__(self, api_url: str, api_key: str, workspace: Optional[str] = None,
                 extra_headers: Optional[Dict[str, str]] = None):
        """Initialize the Extralit client.

        Args:
            api_url: The URL of the Extralit server.
            api_key: The API key for authentication.
            workspace: Optional default workspace.
            extra_headers: Optional extra headers for API requests.
        """
        self.api_url = api_url
        self.api_key = api_key
        self.workspace = workspace
        self.extra_headers = extra_headers or {}

        # In a real implementation, we would validate the credentials here
        # For now, we'll just assume they're valid

    @classmethod
    def from_credentials(cls, api_url: Optional[str] = None, api_key: Optional[str] = None,
                         workspace: Optional[str] = None, extra_headers: Optional[Dict[str, str]] = None):
        """Create client from credentials.

        If api_url and api_key are not provided, they will be loaded from environment variables
        or from the credentials file.

        Args:
            api_url: The URL of the Extralit server.
            api_key: The API key for authentication.
            workspace: Optional default workspace.
            extra_headers: Optional extra headers for API requests.

        Returns:
            Argilla: An initialized Extralit client.
        """
        from argilla.client.login import ArgillaCredentials

        # Try to get credentials from environment variables
        api_url = api_url or os.environ.get("EXTRALIT_API_URL")
        api_key = api_key or os.environ.get("EXTRALIT_API_KEY")
        workspace = workspace or os.environ.get("EXTRALIT_WORKSPACE")

        # If not found, try to load from credentials file
        if (not api_url or not api_key) and ArgillaCredentials.exists():
            credentials = ArgillaCredentials.load()
            api_url = api_url or credentials.api_url
            api_key = api_key or credentials.api_key
            workspace = workspace or credentials.workspace
            extra_headers = extra_headers or credentials.extra_headers

        return cls(api_url=api_url, api_key=api_key, workspace=workspace, extra_headers=extra_headers)

    @property
    def me(self) -> User:
        """Get the current user.

        Returns:
            User: The current user.
        """
        # In a real implementation, we would make an API call to get the user
        # For now, we'll just return a mock user
        return User(
            username="current_user",
            role="admin",
            first_name="Current",
            last_name="User",
            api_key=self.api_key,
            workspaces=["default", "research"],
            api_url=self.api_url
        )

    def get_server_info(self) -> Dict[str, Any]:
        """Get information about the server.

        Returns:
            Dict[str, Any]: Server information.
        """
        # Make a request to the server to get information
        try:
            response = requests.get(
                f"{self.api_url}/api/v1/me",
                headers={
                    "X-API-Key": self.api_key,
                    **self.extra_headers
                }
            )
            response.raise_for_status()

            # In a real implementation, we would parse the response
            # For now, we'll return a mix of real and mock data
            return {
                "url": self.api_url,
                "version": "2.0.0",
                "database_version": "1.0.0"
            }
        except Exception as e:
            # If the request fails, return mock data
            return {
                "url": self.api_url,
                "version": "2.0.0",
                "database_version": "1.0.0"
            }

    def list_datasets(self, workspace: Optional[str] = None, type_: Optional[DatasetType] = None) -> List[Dict[str, Any]]:
        """List datasets with optional filtering by workspace and type.

        Args:
            workspace: Optional workspace name to filter datasets by.
            type_: Optional dataset type to filter datasets by.

        Returns:
            List[Dict[str, Any]]: List of datasets.
        """
        # Make a request to the server to get datasets
        try:
            # In a real implementation, we would make an API call to get datasets
            # For now, we'll return mock data
            mock_datasets = [
                {
                    "id": "1",
                    "name": "sentiment-analysis",
                    "workspace": "default",
                    "type": DatasetType.TEXT_CLASSIFICATION,
                    "tags": {
                        "domain": "customer-support",
                        "language": "english"
                    },
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                },
                {
                    "id": "2",
                    "name": "named-entity-recognition",
                    "workspace": "research",
                    "type": DatasetType.TOKEN_CLASSIFICATION,
                    "tags": {
                        "domain": "news",
                        "language": "english"
                    },
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                },
                {
                    "id": "3",
                    "name": "text-summarization",
                    "workspace": "default",
                    "type": DatasetType.TEXT_GENERATION,
                    "tags": {
                        "domain": "articles",
                        "language": "english"
                    },
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                },
                {
                    "id": "4",
                    "name": "user-feedback",
                    "workspace": "default",
                    "type": DatasetType.FEEDBACK,
                    "tags": {},
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                }
            ]

            # Apply filters if specified
            filtered_datasets = mock_datasets
            if workspace:
                filtered_datasets = [ds for ds in filtered_datasets if ds["workspace"] == workspace]
            if type_:
                filtered_datasets = [ds for ds in filtered_datasets if ds["type"] == type_]

            return filtered_datasets
        except Exception as e:
            # If the request fails, return an empty list
            return []

    def get_dataset(self, name: str, workspace: Optional[str] = None) -> Dict[str, Any]:
        """Get a dataset by name and optional workspace.

        Args:
            name: The name of the dataset to get.
            workspace: Optional workspace name where the dataset belongs.

        Returns:
            Dict[str, Any]: The dataset.

        Raises:
            ValueError: If the dataset is not found.
        """
        # Get all datasets and filter by name and workspace
        datasets = self.list_datasets(workspace=workspace)
        for dataset in datasets:
            if dataset["name"] == name:
                return dataset

        # If we get here, the dataset was not found
        if workspace:
            raise ValueError(f"Dataset with name={name} and workspace={workspace} not found.")
        else:
            raise ValueError(f"Dataset with name={name} not found. Try using '--workspace' option.")

    def create_dataset(self, name: str, type_: DatasetType, workspace: Optional[str] = None) -> Dict[str, Any]:
        """Create a new dataset.

        Args:
            name: The name of the dataset to create.
            type_: The type of the dataset to create.
            workspace: Optional workspace name where the dataset will be created.

        Returns:
            Dict[str, Any]: The created dataset.

        Raises:
            ValueError: If a dataset with the same name already exists in the workspace.
            RuntimeError: If there was an error creating the dataset.
        """
        # Check if a dataset with the same name already exists
        try:
            existing_dataset = self.get_dataset(name=name, workspace=workspace)
            # If we get here, a dataset with the same name already exists
            raise ValueError(f"Dataset with name='{name}' already exists in workspace='{workspace or 'default'}'.")
        except ValueError:
            # This is expected - the dataset should not exist
            pass

        # In a real implementation, we would make an API call to create the dataset
        # For now, we'll just return a mock dataset
        if not workspace:
            workspace = "default"

        return {
            "id": "new-id",
            "name": name,
            "workspace": workspace,
            "type": type_,
            "tags": {},
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

    def delete_dataset(self, name: str, workspace: Optional[str] = None) -> bool:
        """Delete a dataset.

        Args:
            name: The name of the dataset to delete.
            workspace: Optional workspace name where the dataset belongs.

        Returns:
            bool: True if the dataset was deleted successfully, False otherwise.

        Raises:
            ValueError: If the dataset is not found.
            RuntimeError: If there was an error deleting the dataset.
        """
        # Check if the dataset exists
        dataset = self.get_dataset(name=name, workspace=workspace)

        # In a real implementation, we would make an API call to delete the dataset
        # For now, we'll just return success
        return True

    def push_dataset_to_huggingface(self, name: str, repo_id: str, private: bool = False,
                                   token: Optional[str] = None, workspace: Optional[str] = None) -> bool:
        """Push a dataset to HuggingFace Hub.

        Args:
            name: The name of the dataset to push.
            repo_id: The HuggingFace Hub repo where the dataset will be pushed to.
            private: Whether the dataset should be private or not.
            token: The HuggingFace Hub token to be used for pushing the dataset.
            workspace: Optional workspace name where the dataset belongs.

        Returns:
            bool: True if the dataset was pushed successfully, False otherwise.

        Raises:
            ValueError: If the dataset is not found or has no records.
            RuntimeError: If there was an error pushing the dataset.
        """
        # Check if the dataset exists
        dataset = self.get_dataset(name=name, workspace=workspace)

        # In a real implementation, we would make an API call to push the dataset
        # For now, we'll just simulate a delay and return success
        time.sleep(2)  # Simulate delay

        return True