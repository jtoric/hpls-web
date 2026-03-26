"""CRUD endpoints for posts (news articles and calendar events)."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import User
from app.repositories.post_repository import PostRepository
from app.schemas import PostCreate, PostOut, PostUpdate
from app.services.post_service import PostService

router = APIRouter(prefix="/api/posts", tags=["posts"])


def get_post_service(db: Session = Depends(get_db)) -> PostService:
    return PostService(PostRepository(db))


@router.get("")
def list_posts(
    category: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    service: PostService = Depends(get_post_service),
):
    """List published posts with optional category filter and pagination."""
    return service.list_published(category, page, limit)


@router.get("/admin/all")
def list_all_posts(
    category: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    service: PostService = Depends(get_post_service),
    user: User = Depends(get_current_user),
):
    """List all posts including unpublished (admin only)."""
    return service.list_all(category, page, limit)


@router.get("/{slug}", response_model=PostOut)
def get_post(slug: str, service: PostService = Depends(get_post_service)):
    """Get a single post by its URL slug."""
    return service.get_by_slug(slug)


@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    data: PostCreate,
    service: PostService = Depends(get_post_service),
    user: User = Depends(get_current_user),
):
    """Create a new post (admin only). Slug is auto-generated from the title."""
    return service.create(data)


@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    data: PostUpdate,
    service: PostService = Depends(get_post_service),
    user: User = Depends(get_current_user),
):
    """Update an existing post (admin only)."""
    return service.update(post_id, data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    service: PostService = Depends(get_post_service),
    user: User = Depends(get_current_user),
):
    """Delete a post and its attachments (admin only)."""
    service.delete(post_id)
