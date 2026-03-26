"""Pydantic schemas for request/response validation.

Defines all API input (Create/Update) and output (Out) models.
Pydantic automatically validates types and constraints on every request.
"""

import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    """Credentials submitted to POST /api/auth/login."""

    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)


class Token(BaseModel):
    """JWT token returned after successful login."""

    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    """Public representation of a user (no password hash)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


# ---------------------------------------------------------------------------
# Post (News + Calendar)
# ---------------------------------------------------------------------------

class PostCreate(BaseModel):
    """Payload for creating a new post."""

    title: str = Field(..., min_length=1, max_length=255)
    content: str = ""
    excerpt: str = Field(default="", max_length=500)
    featured_image: str | None = None
    category: Literal["news", "calendar"] = "news"
    published: bool = True


class PostUpdate(BaseModel):
    """Payload for updating an existing post. All fields optional."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None
    excerpt: str | None = Field(default=None, max_length=500)
    featured_image: str | None = None
    category: Literal["news", "calendar"] | None = None
    published: bool | None = None


class AttachmentOut(BaseModel):
    """Representation of a file attached to a post or page."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    file_path: str
    file_type: str
    original_name: str
    uploaded_at: datetime


class PostOut(BaseModel):
    """Full post detail including content and attachments."""

    model_config = ConfigDict(from_attributes=True)

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


class PostListOut(BaseModel):
    """Lightweight post representation for list views (no content body)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    excerpt: str
    featured_image: str | None
    category: str
    published: bool
    created_at: datetime


# ---------------------------------------------------------------------------
# Page (static content)
# ---------------------------------------------------------------------------

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class PageUpdate(BaseModel):
    """Payload for updating page content."""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None


class PageCreate(BaseModel):
    """Payload for creating a new static page."""

    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    content: str = ""
    parent_slug: str | None = None
    sort_order: int = Field(default=0, ge=0)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        if not SLUG_PATTERN.match(v):
            raise ValueError("Slug must contain only lowercase letters, numbers, and hyphens")
        return v


class PageOut(BaseModel):
    """Full page detail including content and attachments."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    content: str
    parent_slug: str | None
    sort_order: int
    updated_at: datetime
    attachments: list[AttachmentOut] = []


class PageListOut(BaseModel):
    """Lightweight page representation for list views."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    parent_slug: str | None
    sort_order: int
    updated_at: datetime


# ---------------------------------------------------------------------------
# Document
# ---------------------------------------------------------------------------

class DocumentOut(BaseModel):
    """Representation of a downloadable document."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    file_path: str
    file_size: int
    uploaded_at: datetime


# ---------------------------------------------------------------------------
# Generic
# ---------------------------------------------------------------------------

class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper."""

    items: list[PostListOut]
    total: int
    page: int
    pages: int


class UploadResponse(BaseModel):
    """Response returned after a successful file upload."""

    file_path: str
    original_name: str
    file_type: str
