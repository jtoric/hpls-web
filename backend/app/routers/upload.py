import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.auth import get_current_user
from app.config import (
    ALLOWED_DOC_EXTENSIONS,
    ALLOWED_IMAGE_EXTENSIONS,
    MAX_UPLOAD_SIZE,
    UPLOAD_DIR,
)
from app.models import User
from app.schemas import UploadResponse

router = APIRouter(prefix="/api/upload", tags=["upload"])

ALL_ALLOWED = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_DOC_EXTENSIONS


async def save_upload(file: UploadFile, subfolder: str = "files") -> dict:
    """Save an uploaded file and return its path info."""
    ext = os.path.splitext(file.filename or "")[1].lower()

    # Read file content
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 20MB)")

    # Generate unique filename
    now = datetime.utcnow()
    date_path = now.strftime("%Y/%m")
    unique_name = f"{uuid.uuid4().hex[:12]}{ext}"

    # Create directory
    save_dir = UPLOAD_DIR / subfolder / date_path
    save_dir.mkdir(parents=True, exist_ok=True)

    # Write file
    file_path = save_dir / unique_name
    with open(file_path, "wb") as f:
        f.write(content)

    relative_path = f"/uploads/{subfolder}/{date_path}/{unique_name}"

    # Determine file type
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


@router.post("", response_model=UploadResponse)
async def upload_file(
    file: UploadFile,
    user: User = Depends(get_current_user),
):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALL_ALLOWED:
        raise HTTPException(
            status_code=400,
            detail=f"File type {ext} not allowed. Allowed: {', '.join(ALL_ALLOWED)}",
        )

    # Route to appropriate subfolder
    if ext in ALLOWED_IMAGE_EXTENSIONS:
        subfolder = "images"
    elif ext in ALLOWED_DOC_EXTENSIONS:
        subfolder = "documents"
    else:
        subfolder = "files"

    result = await save_upload(file, subfolder)
    return UploadResponse(**result)
