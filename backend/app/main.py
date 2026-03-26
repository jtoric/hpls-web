from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.config import UPLOAD_DIR
from app.database import Base, engine, get_db
from app.repositories.page_repository import PageRepository
from app.repositories.post_repository import PostRepository
from app.routers import auth, documents, pages, posts, upload
from app.services.search_service import SearchService

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


def get_search_service(db: Session = Depends(get_db)) -> SearchService:
    return SearchService(PostRepository(db), PageRepository(db))


@app.get("/api/search")
def search(q: str = "", service: SearchService = Depends(get_search_service)):
    return service.search(q)
