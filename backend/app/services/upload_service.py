import os
import uuid
from datetime import datetime

from fastapi import HTTPException, UploadFile

from app.config import (
    ALLOWED_DOC_EXTENSIONS,
    ALLOWED_IMAGE_EXTENSIONS,
    MAX_UPLOAD_SIZE,
    UPLOAD_DIR,
)


ALL_ALLOWED = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_DOC_EXTENSIONS


class UploadService:
    async def save(
        self, file: UploadFile, subfolder: str, allowed_extensions: set[str] | None = None
    ) -> dict:
        ext = os.path.splitext(file.filename or "")[1].lower()
        allowed = allowed_extensions or ALL_ALLOWED

        if ext not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"File type {ext} not allowed. Allowed: {', '.join(allowed)}",
            )

        content = await file.read()
        if len(content) > MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 20MB)")

        now = datetime.utcnow()
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
        if ext in ALLOWED_IMAGE_EXTENSIONS:
            return "images"
        if ext in ALLOWED_DOC_EXTENSIONS:
            return "documents"
        return "files"
