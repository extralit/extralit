"""Models for document operations in Argilla."""

import os
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Document(BaseModel):
    """A document in a workspace."""
    id: Optional[UUID] = None
    workspace_id: UUID
    file_path: Optional[str] = None
    url: Optional[str] = None
    pmid: Optional[str] = None
    doi: Optional[str] = None
    inserted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_server_payload(self) -> dict:
        """Convert the document to a server payload."""
        return {
            "workspace_id": str(self.workspace_id),
            "url": self.url,
            "pmid": self.pmid,
            "doi": self.doi,
        }
