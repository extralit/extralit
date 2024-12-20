import base64
from io import BytesIO
import logging
from uuid import UUID
from typing import TYPE_CHECKING, Optional, List, Union

from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, Path, status, Security
from fastapi.responses import StreamingResponse
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import selectinload

from argilla_server.database import get_async_db
from argilla_server.models.database import Document
from argilla_server.security import auth
from argilla_server.models import User, Workspace
from argilla_server.contexts import accounts, datasets, files
from argilla_server.api.policies.v1 import DocumentPolicy, authorize, is_authorized
from argilla_server.api.schemas.v1.documents import DocumentCreateRequest, DocumentListItem

if TYPE_CHECKING:
    from argilla_server.models import Document

_LOGGER = logging.getLogger("documents")

router = APIRouter(tags=["documents"])


@router.post("/documents", status_code=status.HTTP_201_CREATED, response_model=DocumentListItem)
async def upload_document(
    *,
    document_create: DocumentCreateRequest = Depends(),
    file_data: UploadFile = File(None),
    db: AsyncSession = Depends(get_async_db),
    client: Minio = Depends(files.get_minio_client),
    current_user: User = Security(auth.get_current_user)
):
    await authorize(current_user, DocumentPolicy.create())

    workspace = await Workspace.get(db, document_create.workspace_id)
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Workspace with id `{document_create.workspace_id}` not found",
        )
    
    # Save file to S3
    if file_data is not None:
        object_path = files.get_pdf_s3_object_path(document_create.id)
        existing_files = files.list_objects(client, workspace.name, prefix=object_path, include_version=False, recursive=False)
        file_data_bytes = await file_data.read()

        put_object = False
        if existing_files.objects:
            new_file_hash = files.compute_hash(file_data_bytes)
            existing_hashes = {
                existing_file.etag.strip('"') \
                for existing_file in existing_files.objects \
                if existing_file.etag is not None
            }
            
            if new_file_hash not in existing_hashes:
                put_object = True
            else:
                _LOGGER.info(f"Skipping upload document %s with hash already exists", object_path)
        else:
            put_object = True
        
        if put_object:
            response = files.put_object(
                client, bucket=workspace.name, object=object_path, data=file_data_bytes, 
                size=len(file_data_bytes), content_type="application/pdf", 
                metadata=document_create.dict(include={"file_name": True, "pmid": True, "doi": True}))

            document_create.url = files.get_s3_object_url(response.bucket_name, response.object_name)
            if file_data.filename and not document_create.file_name:
                document_create.file_name = file_data.filename
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Document with id `{document_create.id}` already exists",
            )

    elif not document_create.url:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No document file or URL provided",
        )
    
    # Save to `documents` table
    document = await datasets.upsert_document(db, document_create)
    return DocumentListItem.model_validate(document)


@router.get("/documents/by-pmid/{pmid}", response_model=DocumentListItem)
async def get_document_by_pmid(
    *,
    db: AsyncSession = Depends(get_async_db),
    pmid: str,
    current_user: User = Security(auth.get_current_user)
):
    if pmid is None or not isinstance(pmid, str) or not pmid.isnumeric():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with pmid `{pmid}` not found",
        )
    
    query = await db.execute(
        select(Document).where(Document.pmid == pmid)
    )
    await authorize(current_user, DocumentPolicy.get())

    documents = query.fetchone()
    if documents is None or len(documents) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with pmid `{pmid}` not found",
        )
    
    document: Document = documents[0]
    return DocumentListItem.model_validate(document)


@router.get("/documents/by-id/{id}", response_model=DocumentListItem)
async def get_document_by_id(
    *,
    id: UUID = Path(..., title="The UUID of the document to get"),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Security(auth.get_current_user)
):
    if id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id `{id}` not found",
        )
    
    query = await db.execute(
        select(Document).where(Document.id == id)
    )
    await authorize(current_user, DocumentPolicy.get())

    documents = query.fetchone()
    if documents is None or len(documents) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id `{id}` not found",
        )
    
    document: Document = documents[0]
    return DocumentListItem.model_validate(document)


@router.delete("/documents/{document_id}", status_code=status.HTTP_200_OK, response_model=DocumentListItem, 
               description="Delete all documents by workspace_id, or a specific document by id, pmid, doi, or url")
async def delete_document(*,
    db: AsyncSession = Depends(get_async_db),
    document_id: UUID,
    client: Minio = Depends(files.get_minio_client),
    current_user: User = Security(auth.get_current_user)
    ):
    document = await Document.get_or_raise(
        db,
        document_id,
        options=[
            selectinload(Document.workspace),
        ],
    )

    await authorize(current_user, DocumentPolicy.delete(document.workspace_id))

    document = await datasets.delete_document(db, document)
    
    object_path = files.get_pdf_s3_object_path(document.id)
    files.delete_object(client, document.workspace.name, object_path)

    return DocumentListItem.model_validate(document)


@router.get("/documents/workspace/{workspace_id}", status_code=status.HTTP_200_OK, 
            response_model=List[DocumentListItem])
async def list_documents(*,
    db: AsyncSession = Depends(get_async_db),
    workspace_id: UUID = Path(..., title="The UUID of the workspace whose documents will be retrieved"),
    current_user: User = Security(auth.get_current_user)
    ) -> List[DocumentListItem]:
    await authorize(current_user, DocumentPolicy.list(workspace_id))

    documents = await datasets.list_documents(db, workspace_id)

    return [DocumentListItem.model_validate(doc) for doc in documents]