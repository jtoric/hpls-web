from fastapi import APIRouter, Depends, UploadFile, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.repositories.document_repository import DocumentRepository
from app.schemas import DocumentOut
from app.services.document_service import DocumentService
from app.services.upload_service import UploadService

router = APIRouter(prefix="/api/documents", tags=["documents"])


def get_document_service(db: Session = Depends(get_db)) -> DocumentService:
    return DocumentService(DocumentRepository(db), UploadService())


@router.get("", response_model=list[DocumentOut])
def list_documents(service: DocumentService = Depends(get_document_service)):
    return service.list_all()


@router.post("", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_document(
    title: str,
    file: UploadFile,
    service: DocumentService = Depends(get_document_service),
    user: User = Depends(get_current_user),
):
    return await service.upload(title, file)


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    doc_id: int,
    service: DocumentService = Depends(get_document_service),
    user: User = Depends(get_current_user),
):
    service.delete(doc_id)
