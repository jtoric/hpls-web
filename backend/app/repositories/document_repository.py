"""Repository for Document database operations."""

from sqlalchemy.orm import Session

from app.models import Document


class DocumentRepository:
    """Encapsulates all SQL queries related to Document records."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, doc_id: int) -> Document | None:
        return self.db.query(Document).filter(Document.id == doc_id).first()

    def list_all(self) -> list[Document]:
        """Return all documents, newest first."""
        return self.db.query(Document).order_by(Document.uploaded_at.desc()).all()

    def create(self, **kwargs) -> Document:
        doc = Document(**kwargs)
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc

    def delete(self, doc: Document) -> None:
        self.db.delete(doc)
        self.db.commit()
