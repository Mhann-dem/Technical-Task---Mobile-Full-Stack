"""
Authentication utilities
"""

from fastapi import HTTPException, status
from typing import Optional
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def verify_api_key(api_key: Optional[str]) -> bool:
    """
    Verify API key for requests
    
    Args:
        api_key: API key from request header
        
    Returns:
        True if valid, raises HTTPException if invalid
    """
    if not settings.ENABLE_API_KEY:
        return True
    
    if not api_key:
        logger.warning("Request received without API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if api_key != settings.API_KEY:
        logger.warning(f"Invalid API key attempt: {api_key[:5]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return True
