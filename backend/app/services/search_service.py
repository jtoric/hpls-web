"""Service layer for cross-model search."""

from app.repositories.page_repository import PageRepository
from app.repositories.post_repository import PostRepository


class SearchService:
    """Searches across published posts and pages using LIKE queries."""

    def __init__(self, post_repo: PostRepository, page_repo: PageRepository):
        self.post_repo = post_repo
        self.page_repo = page_repo

    def search(self, query: str) -> dict:
        """Return matching posts and pages for the given query string.

        Queries shorter than 2 characters return empty results to avoid
        overly broad matches.
        """
        if len(query) < 2:
            return {"posts": [], "pages": []}

        found_posts = self.post_repo.search(query)
        found_pages = self.page_repo.search(query)

        return {
            "posts": [
                {"id": p.id, "title": p.title, "slug": p.slug, "category": p.category}
                for p in found_posts
            ],
            "pages": [
                {"id": p.id, "title": p.title, "slug": p.slug}
                for p in found_pages
            ],
        }
