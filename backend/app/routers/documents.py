import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import ALLOWED_DOC_EXTENSIONS, MAX_UPLOAD_SIZE, UPLOAD_DIR
from app.database import get_db
from app.models import Document, User
from app.routers.upload import save_upload
from app.schemas import DocumentOut

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.get("", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.uploaded_at.desc()).all()


@router.post("", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_document(
    title: str,
    file: UploadFile,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_DOC_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type {ext} not allowed")

    result = await save_upload(file, "documents")

    doc = Document(
        title=title,
        file_path=result["file_path"],
        file_size=result["file_size"],
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete file from disk
    full_path = UPLOAD_DIR / doc.file_path.lstrip("/uploads/")
    if full_path.exists():
        full_path.unlink()

    db.delete(doc)
    db.commit()
