"""
Image upload endpoint
"""

from fastapi import APIRouter, UploadFile, File, Header, HTTPException, status
from pydantic import BaseModel
import uuid
import os
from typing import Optional
from app.config import settings
from app.utils.validators import validate_file_upload, validate_image
from app.utils.auth import verify_api_key
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


class UploadResponse(BaseModel):
    """Response model for upload endpoint"""
    image_id: str
    filename: str
    size: int
    message: str


@router.post("/upload", response_model=UploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    x_api_key: Optional[str] = Header(None)
):
    """
    Upload an image file
    
    Args:
        file: Image file (JPEG or PNG)
        x_api_key: Optional API key header
        
    Returns:
        UploadResponse with image_id
        
    Raises:
        HTTPException: If file validation fails
    """
    # Verify API key
    verify_api_key(x_api_key)
    
    logger.info(f"Upload request received for file: {file.filename}")
    
    try:
        # Read file content
        contents = await file.read()
        file_size = len(contents)
        
        # Validate file
        validate_file_upload(file.filename, file_size)
        
        # Generate unique image ID
        image_id = str(uuid.uuid4())
        
        # Get file extension
        file_ext = file.filename.split('.')[-1].lower()
        
        # Save file
        file_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}.{file_ext}")
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Validate image
        validate_image(file_path)
        
        logger.info(f"File uploaded successfully: {image_id} ({file.filename})")
        
        return UploadResponse(
            image_id=image_id,
            filename=file.filename,
            size=file_size,
            message="Image uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process upload"
        )
