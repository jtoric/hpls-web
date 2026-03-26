from datetime import datetime

from pydantic import BaseModel


# --- Auth ---
class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# --- Post ---
class PostCreate(BaseModel):
    title: str
    content: str = ""
    excerpt: str = ""
    featured_image: str | None = None
    category: str = "news"
    published: bool = True


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    excerpt: str | None = None
    featured_image: str | None = None
    category: str | None = None
    published: bool | None = None


class AttachmentOut(BaseModel):
    id: int
    file_path: str
    file_type: str
    original_name: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    excerpt: str
    featured_image: str | None
    category: str
    published: bool
    created_at: datetime
    updated_at: datetime
    attachments: list[AttachmentOut] = []

    class Config:
        from_attributes = True


class PostListOut(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: str
    featured_image: str | None
    category: str
    published: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --- Page ---
class PageUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class PageCreate(BaseModel):
    title: str
    slug: str
    content: str = ""
    parent_slug: str | None = None
    sort_order: int = 0


class PageOut(BaseModel):
    id: int
    title: str
    slug: str
    content: str
    parent_slug: str | None
    sort_order: int
    updated_at: datetime
    attachments: list[AttachmentOut] = []

    class Config:
        from_attributes = True


class PageListOut(BaseModel):
    id: int
    title: str
    slug: str
    parent_slug: str | None
    sort_order: int
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Document ---
class DocumentOut(BaseModel):
    id: int
    title: str
    file_path: str
    file_size: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


# --- Generic ---
class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    pages: int


class UploadResponse(BaseModel):
    file_path: str
    original_name: str
    file_type: str
