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

from uuid import UUID
from typing import Optional, Union
from pydantic import BaseModel, Field, ConfigDict


class DocumentCreate(BaseModel):
    id: Optional[UUID] = None
    workspace_id: UUID = Field(..., description="The workspace ID where the document will be uploaded.")
    reference: Optional[str] = Field(None, description="A reference to the document.")
    url: Optional[str] = Field(
        None,
        description="A URL to the PDF document if it is public available online. If the `file_data` is uploaded, this field should be left empty.",
        repr=False,
    )
    file_name: Optional[str] = Field(None, description="The name of the file.")
    pmid: Optional[str] = Field(None, description="The PubMed ID of the document.")
    doi: Optional[str] = Field(None, description="The DOI of the document.")


class DocumentDelete(BaseModel):
    id: Optional[Union[UUID, str]] = None
    url: Optional[str] = None
    pmid: Optional[str] = Field(None, description="The PubMed ID of the document.")
    doi: Optional[str] = Field(None, description="The DOI of the document.")


class DocumentListItem(BaseModel):
    id: UUID
    reference: Optional[str]
    url: Optional[str]
    file_name: Optional[str]
    pmid: Optional[str]
    doi: Optional[str]
    workspace_id: UUID

    model_config = ConfigDict(from_attributes=True)
