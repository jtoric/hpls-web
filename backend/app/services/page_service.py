from fastapi import HTTPException

from app.repositories.page_repository import PageRepository
from app.schemas import PageCreate, PageListOut, PageOut, PageUpdate


class PageService:
    def __init__(self, repo: PageRepository):
        self.repo = repo

    def list_all(self) -> list[PageListOut]:
        pages = self.repo.list_all()
        return [PageListOut.model_validate(p) for p in pages]

    def get_by_slug(self, slug: str) -> PageOut:
        page = self.repo.get_by_slug(slug)
        if not page:
            raise HTTPException(status_code=404, detail="Page not found")
        return page

    def create(self, data: PageCreate) -> PageOut:
        existing = self.repo.get_by_slug(data.slug)
        if existing:
            raise HTTPException(status_code=400, detail="Page with this slug already exists")
        page = self.repo.create(**data.model_dump())
        return page

    def update(self, page_id: int, data: PageUpdate) -> PageOut:
        page = self.repo.get_by_id(page_id)
        if not page:
            raise HTTPException(status_code=404, detail="Page not found")
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(page, update_data)
