"""Application configuration.

All settings are read from environment variables with sensible defaults
for local development. In production, set SECRET_KEY to a strong random value.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'hpls.db'}")

# JWT settings – MUST override SECRET_KEY in production
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24h

# Upload constraints
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_DOC_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"}
MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20 MB
