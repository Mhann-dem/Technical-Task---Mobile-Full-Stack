"""
Validation utilities for file uploads and data
"""

import os
from pathlib import Path
from PIL import Image
from fastapi import HTTPException, status
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def validate_file_upload(filename: str, file_size: int) -> bool:
    """
    Validate uploaded file
    
    Args:
        filename: Name of the uploaded file
        file_size: Size of the file in bytes
        
    Returns:
        True if valid
        
    Raises:
        HTTPException if validation fails
    """
    # Check file size
    if file_size > settings.MAX_FILE_SIZE:
        logger.warning(f"File size exceeds limit: {file_size} > {settings.MAX_FILE_SIZE}")
        raise HTTPException(
            status_code=status.HTTP_413_PAYLOAD_TOO_LARGE,
            detail=f"File size exceeds maximum of {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Check file extension
    file_ext = filename.split('.')[-1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        logger.warning(f"Invalid file extension: {file_ext}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    return True


def validate_image(file_path: str) -> bool:
    """
    Validate that file is a valid image
    
    Args:
        file_path: Path to the image file
        
    Returns:
        True if valid image
        
    Raises:
        HTTPException if not a valid image
    """
    try:
        with Image.open(file_path) as img:
            img.verify()
        logger.info(f"Image validation successful: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Image validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or corrupted image file"
        )


def image_exists(image_id: str) -> bool:
    """
    Check if image exists in storage
    
    Args:
        image_id: Image ID to check
        
    Returns:
        True if image exists
    """
    image_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}.jpg")
    exists = os.path.exists(image_path) or os.path.exists(
        os.path.join(settings.UPLOAD_DIR, f"{image_id}.png")
    )
    return exists
