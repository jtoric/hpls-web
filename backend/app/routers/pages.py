"""CRUD endpoints for static pages."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.repositories.page_repository import PageRepository
from app.schemas import PageCreate, PageListOut, PageOut, PageUpdate
from app.services.page_service import PageService

router = APIRouter(prefix="/api/pages", tags=["pages"])


def get_page_service(db: Session = Depends(get_db)) -> PageService:
    return PageService(PageRepository(db))


@router.get("", response_model=list[PageListOut])
def list_pages(service: PageService = Depends(get_page_service)):
    """List all static pages grouped by section."""
    return service.list_all()


@router.get("/{slug}", response_model=PageOut)
def get_page(slug: str, service: PageService = Depends(get_page_service)):
    """Get a single page by its URL slug."""
    return service.get_by_slug(slug)


@router.post("", response_model=PageOut, status_code=status.HTTP_201_CREATED)
def create_page(
    data: PageCreate,
    service: PageService = Depends(get_page_service),
    user: User = Depends(get_current_user),
):
    """Create a new static page (admin only)."""
    return service.create(data)


@router.put("/{page_id}", response_model=PageOut)
def update_page(
    page_id: int,
    data: PageUpdate,
    service: PageService = Depends(get_page_service),
    user: User = Depends(get_current_user),
):
    """Update page title or content (admin only)."""
    return service.update(page_id, data)
