from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Page, User
from app.schemas import PageCreate, PageListOut, PageOut, PageUpdate

router = APIRouter(prefix="/api/pages", tags=["pages"])


@router.get("", response_model=list[PageListOut])
def list_pages(db: Session = Depends(get_db)):
    return db.query(Page).order_by(Page.parent_slug, Page.sort_order).all()


@router.get("/{slug}", response_model=PageOut)
def get_page(slug: str, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.slug == slug).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page


@router.post("", response_model=PageOut, status_code=status.HTTP_201_CREATED)
def create_page(
    data: PageCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    existing = db.query(Page).filter(Page.slug == data.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Page with this slug already exists")
    page = Page(**data.model_dump())
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


@router.put("/{page_id}", response_model=PageOut)
def update_page(
    page_id: int,
    data: PageUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    page = db.query(Page).filter(Page.id == page_id).first()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(page, key, value)
    db.commit()
    db.refresh(page)
    return page
