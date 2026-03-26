"""Service layer for document management."""

import logging

from fastapi import HTTPException, UploadFile, status

from app.config import ALLOWED_DOC_EXTENSIONS, UPLOAD_DIR
from app.repositories.document_repository import DocumentRepository
from app.schemas import DocumentOut
from app.services.upload_service import UploadService

logger = logging.getLogger(__name__)


class DocumentService:
    """Business logic for uploading, listing, and deleting documents."""

    def __init__(self, repo: DocumentRepository, upload_service: UploadService):
        self.repo = repo
        self.upload_service = upload_service

    def list_all(self) -> list[DocumentOut]:
        """Return all documents, newest first."""
        docs = self.repo.list_all()
        return [DocumentOut.model_validate(d) for d in docs]

    async def upload(self, title: str, file: UploadFile) -> DocumentOut:
        """Save the uploaded file to disk and record it in the database."""
        result = await self.upload_service.save(file, "documents", ALLOWED_DOC_EXTENSIONS)
        doc = self.repo.create(
            title=title,
            file_path=result["file_path"],
            file_size=result["file_size"],
        )
        return doc

    def delete(self, doc_id: int) -> None:
        """Remove document record from DB and delete the file from disk.

        Raises:
            HTTPException(404): If no document with this ID exists.
        """
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

        # Safely resolve path relative to UPLOAD_DIR to prevent path traversal.
        relative = doc.file_path.removeprefix("/uploads/")
        full_path = (UPLOAD_DIR / relative).resolve()

        # Ensure the resolved path is still within UPLOAD_DIR.
        if full_path.is_relative_to(UPLOAD_DIR.resolve()) and full_path.exists():
            try:
                full_path.unlink()
            except OSError:
                logger.warning("Failed to delete file %s", full_path)

        self.repo.delete(doc)
