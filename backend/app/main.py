from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import UPLOAD_DIR
from app.database import Base, engine
from app.routers import auth, documents, pages, posts, upload

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HPLS Powerlifting API", version="1.0.0")

# CORS - allow Vue dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Register routers
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(pages.router)
app.include_router(documents.router)
app.include_router(upload.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/search")
def search(q: str = ""):
    """Simple search across posts and pages."""
    if len(q) < 2:
        return {"posts": [], "pages": []}

    from sqlalchemy.orm import Session
    from app.database import SessionLocal
    from app.models import Post, Page

    db = SessionLocal()
    try:
        term = f"%{q}%"
        found_posts = (
            db.query(Post)
            .filter(Post.published == True, (Post.title.ilike(term) | Post.content.ilike(term)))
            .order_by(Post.created_at.desc())
            .limit(10)
            .all()
        )
        found_pages = (
            db.query(Page)
            .filter(Page.title.ilike(term) | Page.content.ilike(term))
            .limit(10)
            .all()
        )
        return {
            "posts": [{"id": p.id, "title": p.title, "slug": p.slug, "category": p.category} for p in found_posts],
            "pages": [{"id": p.id, "title": p.title, "slug": p.slug} for p in found_pages],
        }
    finally:
        db.close()
