from fastapi import HTTPException, UploadFile

from app.config import ALLOWED_DOC_EXTENSIONS, UPLOAD_DIR
from app.repositories.document_repository import DocumentRepository
from app.schemas import DocumentOut
from app.services.upload_service import UploadService


class DocumentService:
    def __init__(self, repo: DocumentRepository, upload_service: UploadService):
        self.repo = repo
        self.upload_service = upload_service

    def list_all(self) -> list[DocumentOut]:
        docs = self.repo.list_all()
        return [DocumentOut.model_validate(d) for d in docs]

    async def upload(self, title: str, file: UploadFile) -> DocumentOut:
        result = await self.upload_service.save(file, "documents", ALLOWED_DOC_EXTENSIONS)
        doc = self.repo.create(
            title=title,
            file_path=result["file_path"],
            file_size=result["file_size"],
        )
        return doc

    def delete(self, doc_id: int) -> None:
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        full_path = UPLOAD_DIR / doc.file_path.lstrip("/uploads/")
        if full_path.exists():
            full_path.unlink()

        self.repo.delete(doc)
