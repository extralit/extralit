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

import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from uuid import UUID

import httpx

from argilla._api._base import ResourceAPI
from argilla._exceptions._api import api_error_handler
from argilla._models._workspace import WorkspaceModel
from argilla._models._files import ListObjectsResponse, ObjectMetadata, FileObjectResponse
from argilla._models._documents import Document

# Define fallback constants
DEFAULT_SCHEMA_S3_PATH = "schemas/"

__all__ = ["WorkspacesAPI"]


class WorkspacesAPI(ResourceAPI[WorkspaceModel]):
    http_client: httpx.Client
    url_stub = "/api/v1/workspaces"

    ################
    # CRUD methods #
    ################

    @api_error_handler
    def create(self, workspace: WorkspaceModel) -> WorkspaceModel:
        # TODO: Unify API endpoint
        response = self.http_client.post(url="/api/v1/workspaces", json={"name": workspace.name})
        response.raise_for_status()
        response_json = response.json()
        workspace = self._model_from_json(json_workspace=response_json)
        self._log_message(message=f"Created workspace {workspace.name}")
        return workspace

    @api_error_handler
    def get(self, workspace_id: UUID) -> WorkspaceModel:
        response = self.http_client.get(url=f"{self.url_stub}/{workspace_id}")
        response.raise_for_status()
        response_json = response.json()
        workspace = self._model_from_json(json_workspace=response_json)
        return workspace

    @api_error_handler
    def delete(self, workspace_id: UUID) -> None:
        response = self.http_client.delete(url=f"{self.url_stub}/{workspace_id}")
        response.raise_for_status()

    def exists(self, workspace_id: UUID) -> bool:
        response = self.http_client.get(url=f"{self.url_stub}/{workspace_id}")
        return response.status_code == 200

    ####################
    # Utility methods #
    ####################

    @api_error_handler
    def list(self) -> List[WorkspaceModel]:
        response = self.http_client.get(url="/api/v1/me/workspaces")
        response.raise_for_status()
        response_json = response.json()
        workspaces = self._model_from_jsons(json_workspaces=response_json["items"])
        self._log_message(message=f"Got {len(workspaces)} workspaces")
        return workspaces

    @api_error_handler
    def list_by_user_id(self, user_id: UUID) -> List[WorkspaceModel]:
        response = self.http_client.get(f"/api/v1/users/{user_id}/workspaces")
        response.raise_for_status()
        response_json = response.json()
        workspaces = self._model_from_jsons(json_workspaces=response_json["items"])
        self._log_message(message=f"Got {len(workspaces)} workspaces")
        return workspaces

    @api_error_handler
    def list_current_user_workspaces(self) -> List[WorkspaceModel]:
        response = self.http_client.get(url="/api/v1/me/workspaces")
        response.raise_for_status()
        response_json = response.json()
        workspaces = self._model_from_jsons(json_workspaces=response_json["items"])
        self._log_message(message=f"Got {len(workspaces)} workspaces")
        return workspaces

    @api_error_handler
    def get_by_name(self, name: str) -> Optional[WorkspaceModel]:
        for workspace in self.list():
            if workspace.name == name:
                self._log_message(message=f"Got workspace {workspace.name}")
                return workspace

    @api_error_handler
    def add_user(self, workspace_id: UUID, user_id: UUID) -> None:
        # TODO: This method is already defined in UsersAPI and should be removed from here
        response = self.http_client.post(f"{self.url_stub}/{workspace_id}/users/{user_id}")
        response.raise_for_status()
        self._log_message(message=f"Added user {user_id} to workspace {workspace_id}")

    ####################
    # File methods #
    ####################

    @api_error_handler
    def list_files(self, workspace_name: str, path: str, recursive: bool = True, include_version: bool = True) -> ListObjectsResponse:
        """List files in a workspace.

        Args:
            workspace_name: The name of the workspace.
            path: The path to list files from.
            recursive: Whether to list files recursively.
            include_version: Whether to include version information.

        Returns:
            A list of files.
        """
        url = f"/api/v1/files/{workspace_name}/{path}"
        params = {
            "recursive": recursive,
            "include_version": include_version,
        }
        response = self.http_client.get(url=url, params=params)
        response.raise_for_status()

        return ListObjectsResponse(**response.json())

    @api_error_handler
    def get_file(self, workspace_name: str, path: str, version_id: Optional[str] = None) -> FileObjectResponse:
        """Get a file from a workspace.

        Args:
            workspace_name: The name of the workspace.
            path: The path of the file.
            version_id: The version ID of the file.

        Returns:
            The file content and metadata.
        """
        url = f"/api/v1/file/{workspace_name}/{path}"
        params = {"version_id": version_id} if version_id else {}
        response = self.http_client.get(url=url, params=params)
        response.raise_for_status()

        # Create a FileObjectResponse with the content
        file_response = FileObjectResponse(content=response.content)

        # Get metadata if available
        if "X-Amz-Meta-Version-Tag" in response.headers:
            metadata = ObjectMetadata(
                bucket_name=workspace_name,
                object_name=path,
                content_type=response.headers.get("Content-Type"),
                etag=response.headers.get("ETag"),
                version_id=version_id,
                version_tag=response.headers.get("X-Amz-Meta-Version-Tag"),
            )
            file_response.metadata = metadata

        return file_response

    @api_error_handler
    def put_file(self, workspace_name: str, path: str, file_path: Path) -> ObjectMetadata:
        """Upload a file to a workspace.

        Args:
            workspace_name: The name of the workspace.
            path: The path to store the file.
            file_path: The local path of the file to upload.

        Returns:
            The metadata of the uploaded file.
        """
        url = f"/api/v1/file/{workspace_name}/{path}"
        file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as file_data:
            files = {"file": (file_name, file_data, "application/octet-stream")}
            response = self.http_client.post(url=url, files=files)
            response.raise_for_status()

        return ObjectMetadata(**response.json())

    @api_error_handler
    def delete_file(self, workspace_name: str, path: str, version_id: Optional[str] = None) -> None:
        """Delete a file from a workspace.

        Args:
            workspace_name: The name of the workspace.
            path: The path of the file to delete.
            version_id: The version ID of the file.
        """
        url = f"/api/v1/file/{workspace_name}/{path}"
        params = {"version_id": version_id} if version_id else {}
        response = self.http_client.delete(url=url, params=params)
        response.raise_for_status()

    @api_error_handler
    def exists_file(self, workspace_name: str, path: str, file_path: Path) -> bool:
        """Check if a file exists in a workspace.

        Args:
            workspace_name: The name of the workspace.
            path: The path of the file.
            file_path: The local path of the file to compare.

        Returns:
            True if the file exists and has the same content, False otherwise.
        """
        try:
            # Try to get the file
            file_response = self.get_file(workspace_name, path)

            # Compare the content with the local file
            with open(file_path, 'rb') as f:
                local_content = f.read()

            return file_response.content == local_content
        except Exception:
            return False

    ####################
    # Document methods #
    ####################

    @api_error_handler
    def add_document(self, document: Document) -> UUID:
        """Add a document to a workspace.

        Args:
            document: The document to add.

        Returns:
            The ID of the added document.
        """
        url = "/api/v1/documents"
        document_payload = document.to_server_payload()

        if document.file_path:
            file_name = os.path.basename(document.file_path)
            with open(document.file_path, 'rb') as file_data:
                files = {
                    "file_data": (file_name, file_data, "application/pdf"),
                }
                response = self.http_client.post(url=url, params=document_payload, files=files)
        else:
            response = self.http_client.post(url=url, params=document_payload)

        response.raise_for_status()
        return UUID(response.json())

    @api_error_handler
    def get_documents(self, workspace_id: UUID) -> List[Document]:
        """Get documents from a workspace.

        Args:
            workspace_id: The ID of the workspace.

        Returns:
            A list of documents.
        """
        url = f"/api/v1/documents/workspace/{workspace_id}"
        response = self.http_client.get(url=url)
        response.raise_for_status()

        documents = []
        for doc_data in response.json():
            doc = Document(
                id=doc_data.get("id"),
                workspace_id=doc_data.get("workspace_id"),
                url=doc_data.get("url"),
                pmid=doc_data.get("pmid"),
                doi=doc_data.get("doi"),
                inserted_at=doc_data.get("inserted_at"),
                updated_at=doc_data.get("updated_at"),
            )
            documents.append(doc)

        return documents

    ####################
    # Schema methods #
    ####################

    @api_error_handler
    def get_schemas(self, workspace_name: str, prefix: str = DEFAULT_SCHEMA_S3_PATH, exclude: Optional[List[str]] = None) -> Any:
        """Get schemas from a workspace.

        Args:
            workspace_name: The name of the workspace.
            prefix: The prefix to filter schemas.
            exclude: List of schema names to exclude.

        Returns:
            A SchemaStructure containing the schemas.
        """
        # Import here to avoid circular imports
        try:
            import pandera as pa
            from extralit.extraction.models import SchemaStructure
        except ImportError:
            raise ImportError("The 'pandera' and 'extralit' packages are required to use schema methods. "
                             "Please install them with 'pip install pandera extralit'.")

        # List all schema files in the workspace
        schema_files = self.list_files(workspace_name, prefix, recursive=True, include_version=True)

        # Filter out excluded schemas
        if exclude:
            schema_files.objects = [obj for obj in schema_files.objects if os.path.basename(obj.object_name) not in exclude]

        # Get the content of each schema file and parse it
        schemas = {}
        for obj in schema_files.objects:
            try:
                # Get the schema file content
                file_response = self.get_file(workspace_name, obj.object_name)

                # Parse the schema from JSON
                schema_json = file_response.content.decode('utf-8')
                schema = pa.DataFrameSchema.from_json(schema_json)

                # Add the schema to the dictionary
                schemas[schema.name] = schema
            except Exception as e:
                self._log_message(f"Error loading schema {obj.object_name}: {str(e)}")

        return SchemaStructure(schemas=list(schemas.values()))

    @api_error_handler
    def add_schema(self, workspace_name: str, schema: Any, prefix: str = DEFAULT_SCHEMA_S3_PATH) -> None:
        """Add a schema to a workspace.

        Args:
            workspace_name: The name of the workspace.
            schema: The schema to add.
            prefix: The prefix to store the schema.
        """
        # Import here to avoid circular imports
        try:
            import pandera as pa
        except ImportError:
            raise ImportError("The 'pandera' package is required to use schema methods. "
                             "Please install it with 'pip install pandera'.")

        # Create the schema file path
        object_path = os.path.join(prefix, schema.name)

        # Create a temporary file with the schema JSON
        temp_dir = Path('/tmp')
        temp_dir.mkdir(exist_ok=True)
        file_path = temp_dir / schema.name

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(schema.to_json())

        # Check if the schema already exists
        try:
            if self.exists_file(workspace_name, object_path, file_path):
                raise ValueError(f"Schema with name=`{schema.name}` already exists in workspace `{workspace_name}`.")

            # Upload the schema file
            self.put_file(workspace_name, object_path, file_path)
        finally:
            # Clean up the temporary file
            if file_path.exists():
                file_path.unlink()

    @api_error_handler
    def update_schemas(self, workspace_name: str, schemas: Any, check_existing: bool = True, prefix: str = DEFAULT_SCHEMA_S3_PATH) -> ListObjectsResponse:
        """Update schemas in a workspace.

        Args:
            workspace_name: The name of the workspace.
            schemas: The schemas to update.
            check_existing: Whether to check if the schema already exists.
            prefix: The prefix to store the schemas.

        Returns:
            A list of updated schema files.
        """
        # Create a temporary directory for schema files
        temp_dir = Path('/tmp')
        temp_dir.mkdir(exist_ok=True)

        # Track the metadata of updated schemas
        updated_schemas = []

        # Process each schema
        for schema in schemas.schemas:
            # Create the schema file path
            object_path = os.path.join(prefix, schema.name)
            file_path = temp_dir / schema.name

            # Write the schema to a temporary file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(schema.to_json())

            try:
                # Check if the schema already exists and is unchanged
                if check_existing and self.exists_file(workspace_name, object_path, file_path):
                    self._log_message(f"Skipping schema name='{schema.name}' update since it's unmodified in workspace '{workspace_name}'.")
                    continue

                # Upload the schema file
                metadata = self.put_file(workspace_name, object_path, file_path)
                updated_schemas.append(metadata)
            except Exception as e:
                raise RuntimeError(f"Error adding schema '{schema.name}' to workspace due to `{e}`.")
            finally:
                # Clean up the temporary file
                if file_path.exists():
                    file_path.unlink()

        return ListObjectsResponse(objects=updated_schemas)

    ####################
    # Private methods #
    ####################

    def _model_from_json(self, json_workspace: Dict) -> WorkspaceModel:
        return WorkspaceModel(
            id=UUID(json_workspace["id"]),
            name=json_workspace["name"],
            inserted_at=self._date_from_iso_format(date=json_workspace["inserted_at"]),
            updated_at=self._date_from_iso_format(date=json_workspace["updated_at"]),
        )

    def _model_from_jsons(self, json_workspaces: List[Dict]) -> List[WorkspaceModel]:
        return list(map(self._model_from_json, json_workspaces))
