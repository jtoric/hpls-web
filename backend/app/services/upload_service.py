"""Service layer for file upload handling.

Files are stored under ``backend/uploads/<subfolder>/YYYY/MM/<uuid>.ext``.
The relative URL path (e.g. ``/uploads/images/2026/03/abc123.jpg``) is stored
in the database and served by FastAPI's ``StaticFiles`` mount.
"""

import os
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, UploadFile, status

from app.config import (
    ALLOWED_DOC_EXTENSIONS,
    ALLOWED_IMAGE_EXTENSIONS,
    MAX_UPLOAD_SIZE,
    UPLOAD_DIR,
)

ALL_ALLOWED = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_DOC_EXTENSIONS


class UploadService:
    """Saves uploaded files to the local filesystem."""

    async def save(
        self, file: UploadFile, subfolder: str, allowed_extensions: set[str] | None = None
    ) -> dict:
        """Read, validate, and persist an uploaded file.

        Returns a dict with ``file_path``, ``original_name``, ``file_type``,
        and ``file_size`` keys.

        Raises:
            HTTPException(400): If the extension or size is not allowed.
        """
        ext = os.path.splitext(file.filename or "")[1].lower()
        allowed = allowed_extensions or ALL_ALLOWED

        if ext not in allowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {ext} not allowed. Allowed: {', '.join(sorted(allowed))}",
            )

        content = await file.read()
        if len(content) > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large (max 20 MB)",
            )

        # Organise uploads by year/month for easier browsing.
        now = datetime.now(timezone.utc)
        date_path = now.strftime("%Y/%m")
        unique_name = f"{uuid.uuid4().hex[:12]}{ext}"

        save_dir = UPLOAD_DIR / subfolder / date_path
        save_dir.mkdir(parents=True, exist_ok=True)

        file_path = save_dir / unique_name
        with open(file_path, "wb") as f:
            f.write(content)

        relative_path = f"/uploads/{subfolder}/{date_path}/{unique_name}"

        if ext in ALLOWED_IMAGE_EXTENSIONS:
            file_type = "image"
        elif ext in ALLOWED_DOC_EXTENSIONS:
            file_type = "document"
        else:
            file_type = "file"

        return {
            "file_path": relative_path,
            "original_name": file.filename or unique_name,
            "file_type": file_type,
            "file_size": len(content),
        }

    def get_subfolder_for_extension(self, ext: str) -> str:
        """Determine the upload subfolder based on file extension."""
        if ext in ALLOWED_IMAGE_EXTENSIONS:
            return "images"
        if ext in ALLOWED_DOC_EXTENSIONS:
            return "documents"
        return "files"
