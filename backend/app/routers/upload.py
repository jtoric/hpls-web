"""Generic file upload endpoint for the WYSIWYG editor.

Uploaded images and documents are saved to the appropriate subfolder
and the URL is returned so the editor can embed them.
"""

import os

from fastapi import APIRouter, Depends, UploadFile

from app.auth import get_current_user
from app.models import User
from app.schemas import UploadResponse
from app.services.upload_service import UploadService

router = APIRouter(prefix="/api/upload", tags=["upload"])


def get_upload_service() -> UploadService:
    return UploadService()


@router.post("", response_model=UploadResponse)
async def upload_file(
    file: UploadFile,
    service: UploadService = Depends(get_upload_service),
    user: User = Depends(get_current_user),
):
    """Upload a file and return its public URL (admin only)."""
    ext = os.path.splitext(file.filename or "")[1].lower()
    subfolder = service.get_subfolder_for_extension(ext)
    result = await service.save(file, subfolder)
    return UploadResponse(**result)
