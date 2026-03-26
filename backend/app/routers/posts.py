import re
import unicodedata
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Post, User
from app.schemas import PostCreate, PostListOut, PostOut, PostUpdate

router = APIRouter(prefix="/api/posts", tags=["posts"])


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")


@router.get("")
def list_posts(
    category: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    q = db.query(Post).filter(Post.published == True)
    if category:
        q = q.filter(Post.category == category)
    total = q.count()
    items = q.order_by(Post.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return {
        "items": [PostListOut.model_validate(p) for p in items],
        "total": total,
        "page": page,
        "pages": ceil(total / limit) if total > 0 else 1,
    }


@router.get("/{slug}", response_model=PostOut)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    slug = slugify(data.title)
    # Ensure unique slug
    base_slug = slug
    counter = 1
    while db.query(Post).filter(Post.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    post = Post(slug=slug, **data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()


# Admin endpoint: list all posts including unpublished
@router.get("/admin/all")
def list_all_posts(
    category: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Post)
    if category:
        q = q.filter(Post.category == category)
    total = q.count()
    items = q.order_by(Post.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return {
        "items": [PostListOut.model_validate(p) for p in items],
        "total": total,
        "page": page,
        "pages": ceil(total / limit) if total > 0 else 1,
    }
