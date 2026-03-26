"""Service layer for post (news / calendar) business logic."""

import re
import unicodedata
from math import ceil

from fastapi import HTTPException, status

from app.repositories.post_repository import PostRepository
from app.schemas import PostCreate, PostListOut, PostOut, PostUpdate


def slugify(text: str) -> str:
    """Convert *text* into a URL-friendly slug.

    Strips diacritics, lowercases, and replaces non-alphanumeric chars with
    hyphens. Example: ``"Državno Prvenstvo 2026"`` → ``"drzavno-prvenstvo-2026"``.
    """
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")


def _paginate(items, total: int, page: int, limit: int) -> dict:
    """Build a standard paginated response dict."""
    return {
        "items": [PostListOut.model_validate(p) for p in items],
        "total": total,
        "page": page,
        "pages": ceil(total / limit) if total > 0 else 1,
    }


class PostService:
    """Business logic for creating, listing, and managing posts."""

    def __init__(self, repo: PostRepository):
        self.repo = repo

    def list_published(self, category: str | None, page: int, limit: int) -> dict:
        """Return paginated published posts, optionally filtered by category."""
        items, total = self.repo.list_published(category, page, limit)
        return _paginate(items, total, page, limit)

    def list_all(self, category: str | None, page: int, limit: int) -> dict:
        """Return paginated posts including unpublished (admin only)."""
        items, total = self.repo.list_all(category, page, limit)
        return _paginate(items, total, page, limit)

    def get_by_slug(self, slug: str) -> PostOut:
        """Fetch a single post by its slug.

        Raises:
            HTTPException(404): If no post with this slug exists.
        """
        post = self.repo.get_by_slug(slug)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return post

    def create(self, data: PostCreate) -> PostOut:
        """Create a new post with an auto-generated unique slug."""
        slug = slugify(data.title)
        base_slug = slug
        counter = 1
        while self.repo.slug_exists(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        post = self.repo.create(slug=slug, **data.model_dump())
        return post

    def update(self, post_id: int, data: PostUpdate) -> PostOut:
        """Update an existing post.

        Raises:
            HTTPException(404): If no post with this ID exists.
        """
        post = self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(post, update_data)

    def delete(self, post_id: int) -> None:
        """Delete a post and its cascade-linked attachments.

        Raises:
            HTTPException(404): If no post with this ID exists.
        """
        post = self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        self.repo.delete(post)
