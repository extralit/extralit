"""Tests for the workspace files API."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest

from argilla._api._workspaces import WorkspacesAPI
from argilla._models._files import ListObjectsResponse, ObjectMetadata, FileObjectResponse
from argilla._models._documents import Document


@pytest.fixture
def workspace_api():
    """Create a mock workspace API."""
    http_client = MagicMock()
    return WorkspacesAPI(http_client=http_client)


def test_list_files(workspace_api):
    """Test listing files in a workspace."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "objects": [
            {
                "bucket_name": "test-workspace",
                "object_name": "test-file.txt",
                "last_modified": "2023-01-01T00:00:00Z",
                "is_latest": True,
                "etag": "test-etag",
                "size": 100,
                "content_type": "text/plain",
                "version_id": "test-version-id",
                "version_tag": "test-version-tag",
                "metadata": {}
            }
        ]
    }
    workspace_api.http_client.get.return_value = mock_response

    # Call the method
    result = workspace_api.list_files("test-workspace", "test-path")

    # Verify the result
    assert isinstance(result, ListObjectsResponse)
    assert len(result.objects) == 1
    assert result.objects[0].bucket_name == "test-workspace"
    assert result.objects[0].object_name == "test-file.txt"

    # Verify the API call
    workspace_api.http_client.get.assert_called_once_with(
        url="/api/v1/files/test-workspace/test-path",
        params={"recursive": True, "include_version": True}
    )


def test_get_file(workspace_api):
    """Test getting a file from a workspace."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"test content"
    mock_response.headers = {
        "Content-Type": "text/plain",
        "ETag": "test-etag",
        "X-Amz-Meta-Version-Tag": "test-version-tag"
    }
    workspace_api.http_client.get.return_value = mock_response

    # Call the method
    result = workspace_api.get_file("test-workspace", "test-file.txt")

    # Verify the result
    assert isinstance(result, FileObjectResponse)
    assert result.content == b"test content"
    assert result.metadata.bucket_name == "test-workspace"
    assert result.metadata.object_name == "test-file.txt"
    assert result.metadata.content_type == "text/plain"
    assert result.metadata.etag == "test-etag"
    assert result.metadata.version_tag == "test-version-tag"

    # Verify the API call
    workspace_api.http_client.get.assert_called_once_with(
        url="/api/v1/file/test-workspace/test-file.txt",
        params={}
    )


def test_put_file(workspace_api, tmp_path):
    """Test uploading a file to a workspace."""
    # Create a test file
    test_file = tmp_path / "test-file.txt"
    test_file.write_text("test content")

    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "bucket_name": "test-workspace",
        "object_name": "test-file.txt",
        "last_modified": "2023-01-01T00:00:00Z",
        "is_latest": True,
        "etag": "test-etag",
        "size": 100,
        "content_type": "text/plain",
        "version_id": "test-version-id",
        "version_tag": "test-version-tag",
        "metadata": {}
    }
    workspace_api.http_client.post.return_value = mock_response

    # Call the method
    result = workspace_api.put_file("test-workspace", "test-file.txt", test_file)

    # Verify the result
    assert isinstance(result, ObjectMetadata)
    assert result.bucket_name == "test-workspace"
    assert result.object_name == "test-file.txt"
    assert result.etag == "test-etag"
    assert result.version_id == "test-version-id"

    # Verify the API call
    workspace_api.http_client.post.assert_called_once()
    assert workspace_api.http_client.post.call_args.kwargs['url'] == "/api/v1/file/test-workspace/test-file.txt"


def test_delete_file(workspace_api):
    """Test deleting a file from a workspace."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    workspace_api.http_client.delete.return_value = mock_response

    # Call the method
    workspace_api.delete_file("test-workspace", "test-file.txt")

    # Verify the API call
    workspace_api.http_client.delete.assert_called_once_with(
        url="/api/v1/file/test-workspace/test-file.txt",
        params={}
    )


def test_add_document(workspace_api):
    """Test adding a document to a workspace."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = "123e4567-e89b-12d3-a456-426614174000"
    workspace_api.http_client.post.return_value = mock_response

    # Create a test document
    document = Document(
        workspace_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        url="https://example.com",
        pmid="12345",
        doi="10.1234/test"
    )

    # Call the method
    result = workspace_api.add_document(document)

    # Verify the result
    assert isinstance(result, UUID)
    assert str(result) == "123e4567-e89b-12d3-a456-426614174000"

    # Verify the API call
    workspace_api.http_client.post.assert_called_once_with(
        url="/api/v1/documents",
        params={
            "workspace_id": "123e4567-e89b-12d3-a456-426614174000",
            "url": "https://example.com",
            "pmid": "12345",
            "doi": "10.1234/test"
        }
    )


def test_get_documents(workspace_api):
    """Test getting documents from a workspace."""
    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "workspace_id": "123e4567-e89b-12d3-a456-426614174000",
            "url": "https://example.com",
            "pmid": "12345",
            "doi": "10.1234/test",
            "inserted_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-01-01T00:00:00Z"
        }
    ]
    workspace_api.http_client.get.return_value = mock_response

    # Call the method
    result = workspace_api.get_documents(UUID("123e4567-e89b-12d3-a456-426614174000"))

    # Verify the result
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Document)
    assert result[0].url == "https://example.com"
    assert result[0].pmid == "12345"
    assert result[0].doi == "10.1234/test"

    # Verify the API call
    workspace_api.http_client.get.assert_called_once_with(
        url="/api/v1/documents/workspace/123e4567-e89b-12d3-a456-426614174000"
    )
