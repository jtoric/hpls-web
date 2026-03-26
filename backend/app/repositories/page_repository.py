"""Repository for Page database operations."""

from sqlalchemy.orm import Session

from app.models import Page

# Fields that may be updated via the API.
UPDATABLE_FIELDS = {"title", "content"}


class PageRepository:
    """Encapsulates all SQL queries related to Page records."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_slug(self, slug: str) -> Page | None:
        return self.db.query(Page).filter(Page.slug == slug).first()

    def get_by_id(self, page_id: int) -> Page | None:
        return self.db.query(Page).filter(Page.id == page_id).first()

    def list_all(self) -> list[Page]:
        """Return all pages ordered by section and then sort_order."""
        return self.db.query(Page).order_by(Page.parent_slug, Page.sort_order).all()

    def create(self, **kwargs) -> Page:
        page = Page(**kwargs)
        self.db.add(page)
        self.db.commit()
        self.db.refresh(page)
        return page

    def update(self, page: Page, data: dict) -> Page:
        """Update only whitelisted fields to prevent mass-assignment."""
        for key, value in data.items():
            if key in UPDATABLE_FIELDS:
                setattr(page, key, value)
        self.db.commit()
        self.db.refresh(page)
        return page

    def search(self, term: str, limit: int = 10) -> list[Page]:
        """Full-text-like search on title and content (LIKE query)."""
        pattern = f"%{term}%"
        return (
            self.db.query(Page)
            .filter(Page.title.ilike(pattern) | Page.content.ilike(pattern))
            .limit(limit)
            .all()
        )
