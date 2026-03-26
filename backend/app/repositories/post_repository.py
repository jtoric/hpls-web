"""Repository for Post database operations."""

from sqlalchemy.orm import Session

from app.models import Post

# Fields that may be updated via the API. Prevents mass-assignment of
# internal columns like ``id``, ``slug``, or ``created_at``.
UPDATABLE_FIELDS = {"title", "content", "excerpt", "featured_image", "category", "published"}


class PostRepository:
    """Encapsulates all SQL queries related to Post records."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_slug(self, slug: str) -> Post | None:
        return self.db.query(Post).filter(Post.slug == slug).first()

    def get_by_id(self, post_id: int) -> Post | None:
        return self.db.query(Post).filter(Post.id == post_id).first()

    def list_published(
        self, category: str | None = None, page: int = 1, limit: int = 10
    ) -> tuple[list[Post], int]:
        """Return published posts, optionally filtered by category."""
        q = self.db.query(Post).filter(Post.published == True)
        if category:
            q = q.filter(Post.category == category)
        total = q.count()
        items = q.order_by(Post.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
        return items, total

    def list_all(
        self, category: str | None = None, page: int = 1, limit: int = 20
    ) -> tuple[list[Post], int]:
        """Return all posts (including unpublished) for the admin panel."""
        q = self.db.query(Post)
        if category:
            q = q.filter(Post.category == category)
        total = q.count()
        items = q.order_by(Post.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
        return items, total

    def slug_exists(self, slug: str) -> bool:
        return self.db.query(Post).filter(Post.slug == slug).first() is not None

    def create(self, **kwargs) -> Post:
        post = Post(**kwargs)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update(self, post: Post, data: dict) -> Post:
        """Update only whitelisted fields to prevent mass-assignment."""
        for key, value in data.items():
            if key in UPDATABLE_FIELDS:
                setattr(post, key, value)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()

    def search(self, term: str, limit: int = 10) -> list[Post]:
        """Full-text-like search on title and content (LIKE query)."""
        pattern = f"%{term}%"
        return (
            self.db.query(Post)
            .filter(Post.published == True, (Post.title.ilike(pattern) | Post.content.ilike(pattern)))
            .order_by(Post.created_at.desc())
            .limit(limit)
            .all()
        )
