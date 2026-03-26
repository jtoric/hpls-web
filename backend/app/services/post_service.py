import re
import unicodedata
from math import ceil

from fastapi import HTTPException

from app.repositories.post_repository import PostRepository
from app.schemas import PostCreate, PostListOut, PostOut, PostUpdate


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")


class PostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    def list_published(self, category: str | None, page: int, limit: int) -> dict:
        items, total = self.repo.list_published(category, page, limit)
        return {
            "items": [PostListOut.model_validate(p) for p in items],
            "total": total,
            "page": page,
            "pages": ceil(total / limit) if total > 0 else 1,
        }

    def list_all(self, category: str | None, page: int, limit: int) -> dict:
        items, total = self.repo.list_all(category, page, limit)
        return {
            "items": [PostListOut.model_validate(p) for p in items],
            "total": total,
            "page": page,
            "pages": ceil(total / limit) if total > 0 else 1,
        }

    def get_by_slug(self, slug: str) -> PostOut:
        post = self.repo.get_by_slug(slug)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    def create(self, data: PostCreate) -> PostOut:
        slug = slugify(data.title)
        base_slug = slug
        counter = 1
        while self.repo.slug_exists(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        post = self.repo.create(slug=slug, **data.model_dump())
        return post

    def update(self, post_id: int, data: PostUpdate) -> PostOut:
        post = self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(post, update_data)

    def delete(self, post_id: int) -> None:
        post = self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        self.repo.delete(post)
