"""
Image analysis endpoint
"""

from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from typing import List
from app.utils.validators import image_exists
from app.utils.auth import verify_api_key
from app.utils.analysis import MockAnalyzer
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


class AnalysisRequest(BaseModel):
    """Request model for analysis endpoint"""
    image_id: str


class AnalysisResponse(BaseModel):
    """Response model for analysis endpoint"""
    image_id: str
    skin_type: str
    detected_issues: List[str]
    confidence: float


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(
    request: AnalysisRequest,
    x_api_key: str = Header(...)
):
    """
    Analyze an uploaded image
    
    Args:
        request: AnalysisRequest with image_id
        x_api_key: API key header (required)
        
    Returns:
        AnalysisResponse with analysis results
        
    Raises:
        HTTPException: If image not found or analysis fails
    """
    # Verify API key
    verify_api_key(x_api_key)
    
    logger.info(f"Analysis request received for image: {request.image_id}")
    
    # Check if image exists
    if not image_exists(request.image_id):
        logger.warning(f"Image not found: {request.image_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with ID '{request.image_id}' not found"
        )
    
    try:
        # Perform analysis using mock analyzer
        analysis_result = MockAnalyzer.analyze_image(request.image_id)
        
        logger.info(f"Analysis completed for {request.image_id}")
        
        return AnalysisResponse(
            image_id=analysis_result["image_id"],
            skin_type=analysis_result["skin_type"],
            detected_issues=analysis_result["detected_issues"],
            confidence=analysis_result["confidence"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed for {request.image_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze image"
        )
