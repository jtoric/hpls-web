from sqlalchemy.orm import Session

from app.models import Page


class PageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_slug(self, slug: str) -> Page | None:
        return self.db.query(Page).filter(Page.slug == slug).first()

    def get_by_id(self, page_id: int) -> Page | None:
        return self.db.query(Page).filter(Page.id == page_id).first()

    def list_all(self) -> list[Page]:
        return self.db.query(Page).order_by(Page.parent_slug, Page.sort_order).all()

    def create(self, **kwargs) -> Page:
        page = Page(**kwargs)
        self.db.add(page)
        self.db.commit()
        self.db.refresh(page)
        return page

    def update(self, page: Page, data: dict) -> Page:
        for key, value in data.items():
            setattr(page, key, value)
        self.db.commit()
        self.db.refresh(page)
        return page

    def search(self, term: str, limit: int = 10) -> list[Page]:
        pattern = f"%{term}%"
        return (
            self.db.query(Page)
            .filter(Page.title.ilike(pattern) | Page.content.ilike(pattern))
            .limit(limit)
            .all()
        )
