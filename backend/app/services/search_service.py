from app.repositories.page_repository import PageRepository
from app.repositories.post_repository import PostRepository


class SearchService:
    def __init__(self, post_repo: PostRepository, page_repo: PageRepository):
        self.post_repo = post_repo
        self.page_repo = page_repo

    def search(self, query: str) -> dict:
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
