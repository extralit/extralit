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
from urllib.parse import urlparse, unquote
from typing import Optional, Dict, Any
import uuid

from pydantic import Field
from argilla._models import ResourceModel

class DocumentModel(ResourceModel):
    """Schema for documents attached to datasets."""

    file_name: str = Field(...)
    reference: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    url: Optional[str] = None
    file_path: Optional[str] = Field(None, description="Local file path")
    workspace_id: Optional[uuid.UUID] = Field(None, description="The workspace ID the document belongs to")

    @classmethod
    def from_file(cls, file_path: str, id: Optional[uuid.UUID]=None, **kwargs) -> "DocumentModel":
        """Create a DocumentModel from a file path."""
        url = None

        if os.path.exists(file_path):
            file_name = file_path.split("/")[-1]

        elif urlparse(file_path).scheme:
            url = file_path
            parsed_url = urlparse(file_path)
            path = parsed_url.path
            file_name = unquote(path).split('/')[-1]

        else:
            raise ValueError(f"File path {file_path} does not exist")

        return cls(
            id=id or uuid.uuid4(),
            file_path=None,
            file_name=file_name,
            url=url,
            **kwargs
        )

    def to_server_payload(self) -> Dict[str, Any]:
        """Create the payload for sending to the server."""
        json = {
            "url": self.url,
            "file_name": self.file_name,
            "pmid": self.pmid,
            "doi": self.doi,
            "reference": self.reference,
            "workspace_id": str(self.workspace_id) if self.workspace_id else None,
        }
        if self.id:
            json["id"] = str(self.id)

        return json
