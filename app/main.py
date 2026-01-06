"""
FastAPI Backend Service for Image Analysis
Handles image uploads and mock analysis for mobile applications
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from typing import Optional
import uuid
import os
from pathlib import Path

from app.routes.upload import router as upload_router
from app.routes.analyze import router as analyze_router
from app.config import settings
from app.utils.auth import verify_api_key
from app.utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Image Analysis API",
    description="Backend service for image upload and analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

# Include routers
app.include_router(upload_router, prefix="/api", tags=["Image Upload"])
app.include_router(analyze_router, prefix="/api", tags=["Analysis"])


@app.get("/")
def read_root():
    """Root endpoint - API health check"""
    logger.info("Health check request received")
    return {
        "message": "Image Analysis API is running",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /api/upload",
            "analyze": "POST /api/analyze",
            "health": "GET /"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint called")
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Image Analysis API")
    uvicorn.run(app, host="0.0.0.0", port=8000)
