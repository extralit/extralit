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
from typing import Dict, List, Optional
from uuid import UUID
import httpx

from argilla._api._base import ResourceAPI
from argilla._exceptions._api import api_error_handler
from argilla._models._document import DocumentModel

class DocumentsAPI(ResourceAPI[DocumentModel]):
    """API for managing documents."""

    http_client: httpx.Client
    url_stub = "/api/v1/documents"

    @api_error_handler
    def create(self, document: DocumentModel) -> DocumentModel:
        """Create a new document."""
        files = None
        if document.file_path and os.path.exists(document.file_path):
            files = {
                "file_data": (document.file_name, open(document.file_path, 'rb'), "application/pdf")
            }

        response = self.http_client.post(
            url=self.url_stub,
            params=document.to_server_payload(),
            files=files
        )
        response.raise_for_status()
        response_json = response.json()
        doc = self._model_from_json(response_json)
        self._log_message(f"Created document {doc.id}")
        return doc


    @api_error_handler
    def delete(self, document: DocumentModel) -> None:
        """Delete a document."""
        response = self.http_client.delete(
            url=f"{self.url_stub}/{document.id}", 
        )
        response.raise_for_status()
        self._log_message(f"Deleted document {document.id}")


    @api_error_handler
    def list(self, workspace_id: Optional[UUID] = None) -> List[DocumentModel]:
        """List documents, optionally filtered by workspace."""
        if workspace_id:
            url = f"{self.url_stub}/workspace/{workspace_id}"
        else:
            url = self.url_stub

        response = self.http_client.get(url)
        response.raise_for_status()
        response_json = response.json()
        docs = [self._model_from_json(doc) for doc in response_json]
        return docs


    def _model_from_json(self, json_doc: Dict) -> DocumentModel:
        """Convert JSON response to DocumentModel."""
        return DocumentModel(**json_doc)
