"""SQLAlchemy ORM models.

Each class maps to a database table. Relationships are defined with
``cascade="all, delete-orphan"`` so that deleting a parent automatically
removes its attachments.
"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


def _utcnow() -> datetime:
    """Return the current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)


class User(Base):
    """Admin user account (only admins can log in)."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=_utcnow)


class Post(Base):
    """A news article or calendar event.

    The ``category`` column distinguishes between ``"news"`` and ``"calendar"``.
    """

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text, default="")
    excerpt = Column(String(500), default="")
    featured_image = Column(String(500), nullable=True)
    category = Column(String(20), nullable=False, default="news")
    published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    attachments = relationship(
        "Attachment", back_populates="post", cascade="all, delete-orphan"
    )


class Page(Base):
    """A static content page (e.g. Rekordi, Poredak, O nama sub-pages).

    Pages with ``parent_slug`` set belong to a section (e.g. ``"o-nama"``).
    """

    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text, default="")
    parent_slug = Column(String(255), nullable=True)
    sort_order = Column(Integer, default=0)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    attachments = relationship(
        "Attachment", back_populates="page", cascade="all, delete-orphan"
    )


class Document(Base):
    """A downloadable file (PDF, DOCX, etc.) listed on the Dokumenti page."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=_utcnow)


class Attachment(Base):
    """A file attached to a specific Post or Page."""

    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=True)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), default="")
    original_name = Column(String(255), default="")
    uploaded_at = Column(DateTime, default=_utcnow)

    post = relationship("Post", back_populates="attachments")
    page = relationship("Page", back_populates="attachments")
