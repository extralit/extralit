# Copyright 2024-present, Extralit Labs, Inc.
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
from typing import Any, Dict, Optional
from urllib.parse import unquote, urlparse
from uuid import UUID
import uuid

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Schema for the `Document` model.

    Args:
        url: The URL of the document. Optional.
        file_data: The file data of the document. Required.
        file_name: The file name of the document. Required.
        pmid: The PMID of the document. Optional.
        doi: The DOI of the document. Optional.
        workspace_id: The workspace ID of the document. Required.
    """

    id: Optional[UUID] = Field(
        default_factory=uuid.uuid4, description="The ID of the document, which gets assigned randomly if not provided."
    )
    file_name: Optional[str] = Field(None)
    reference: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    url: Optional[str] = None
    file_path: Optional[str] = Field(None, description="Local file path")
    workspace_id: Optional[UUID] = Field(None, description="The workspace ID to which the document belongs to")

    @classmethod
    def from_file(
        cls,
        file_path: str,
        *,
        reference: str,
        id: Optional[str] = None,
        pmid: Optional[str] = None,
        doi: Optional[str] = None,
        workspace_id: Optional[UUID] = None,
    ) -> "Document":
        url = None

        if os.path.exists(file_path):
            file_name = file_path.split("/")[-1]

        elif urlparse(file_path).scheme:
            file_path = None
            url = file_path
            parsed_url = urlparse(file_path)
            path = parsed_url.path
            file_name = unquote(path).split("/")[-1]
        else:
            raise ValueError(f"File path {file_path} does not exist")

        return cls(
            file_path=file_path,
            reference=reference,
            file_name=file_name if isinstance(file_name, str) else None,
            url=url if isinstance(url, str) else None,
            id=id or uuid.uuid4(),
            pmid=str(pmid) if isinstance(pmid, int) or isinstance(pmid, str) and len(pmid) > 3 else None,
            doi=doi if isinstance(doi, str) else None,
            workspace_id=workspace_id,
        )

    def to_server_payload(self) -> Dict[str, Any]:
        """Method that will be used to create the payload that will be sent to Argilla
        to create a field in the `FeedbackDataset`.
        """
        json = {
            "url": self.url,
            "file_name": self.file_name,
            "pmid": self.pmid,
            "doi": self.doi,
            "reference": self.reference,
            "workspace_id": str(self.workspace_id),
        }
        if isinstance(self.id, UUID):
            json["id"] = str(self.id)

        return json

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, file_name={self.file_name!r}, pmid={self.pmid!r}, doi={self.doi!r}, workspace_id={self.workspace_id!r})"
