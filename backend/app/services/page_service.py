"""Service layer for static page business logic."""

from fastapi import HTTPException, status

from app.repositories.page_repository import PageRepository
from app.schemas import PageCreate, PageListOut, PageOut, PageUpdate


class PageService:
    """Business logic for listing and editing static pages."""

    def __init__(self, repo: PageRepository):
        self.repo = repo

    def list_all(self) -> list[PageListOut]:
        """Return all pages grouped by parent section."""
        pages = self.repo.list_all()
        return [PageListOut.model_validate(p) for p in pages]

    def get_by_slug(self, slug: str) -> PageOut:
        """Fetch a single page by slug.

        Raises:
            HTTPException(404): If no page with this slug exists.
        """
        page = self.repo.get_by_slug(slug)
        if not page:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
        return page

    def create(self, data: PageCreate) -> PageOut:
        """Create a new static page.

        Raises:
            HTTPException(400): If a page with this slug already exists.
        """
        existing = self.repo.get_by_slug(data.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Page with this slug already exists",
            )
        page = self.repo.create(**data.model_dump())
        return page

    def update(self, page_id: int, data: PageUpdate) -> PageOut:
        """Update an existing page's title or content.

        Raises:
            HTTPException(404): If no page with this ID exists.
        """
        page = self.repo.get_by_id(page_id)
        if not page:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(page, update_data)
