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
    return service.list_published(category, page, limit)


@router.get("/admin/all")
def list_all_posts(
    category: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    service: PostService = Depends(get_post_service),
    user: User = Depends(get_current_user),
):
    return service.list_all(category, page, limit)


@router.get("/{slug}", response_model=PostOut)
def get_post(slug: str, service: PostService = Depends(get_post_service)):
    return service.get_by_slug(slug)


@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    data: PostCreate,
    service: PostService = Depends(get_post_service),
    user: User = Depends(get_current_user),
):
    return service.create(data)


@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    data: PostUpdate,
    service: PostService = Depends(get_post_service),
    user: User = Depends(get_current_user),
):
    return service.update(post_id, data)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    service: PostService = Depends(get_post_service),
    user: User = Depends(get_current_user),
):
    service.delete(post_id)
