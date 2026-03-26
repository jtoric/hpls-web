from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Post(Base):
    """News articles and calendar events."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text, default="")
    excerpt = Column(String(500), default="")
    featured_image = Column(String(500), nullable=True)
    category = Column(String(20), nullable=False, default="news")  # news | calendar
    published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attachments = relationship("Attachment", back_populates="post", cascade="all, delete-orphan")


class Page(Base):
    """Static pages (Rekordi, Poredak, O nama/*, Kontakt)."""

    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text, default="")
    parent_slug = Column(String(255), nullable=True)  # e.g. "o-nama" for sub-pages
    sort_order = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attachments = relationship("Attachment", back_populates="page", cascade="all, delete-orphan")


class Document(Base):
    """Downloadable documents (PDFs etc.)."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class Attachment(Base):
    """Files attached to posts or pages."""

    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=True)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), default="")  # image, document, file
    original_name = Column(String(255), default="")
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="attachments")
    page = relationship("Page", back_populates="attachments")
