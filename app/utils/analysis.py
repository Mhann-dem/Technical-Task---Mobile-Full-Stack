"""
Mock analysis logic for image processing
"""

import random
from typing import Dict, List
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class MockAnalyzer:
    """
    Mock analyzer for image analysis
    In production, this would integrate with actual AI/ML models
    """
    
    SKIN_TYPES = ["Oily", "Dry", "Combination", "Sensitive", "Normal"]
    POSSIBLE_ISSUES = [
        "Acne",
        "Hyperpigmentation",
        "Wrinkles",
        "Dullness",
        "Redness",
        "Texture Issues",
        "None"
    ]
    
    @staticmethod
    def analyze_image(image_id: str) -> Dict:
        """
        Perform mock analysis on image
        
        Args:
            image_id: ID of the image to analyze
            
        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Starting mock analysis for image: {image_id}")
        
        # Generate mock results
        skin_type = random.choice(MockAnalyzer.SKIN_TYPES)
        num_issues = random.randint(0, 2)
        detected_issues = random.sample(
            MockAnalyzer.POSSIBLE_ISSUES,
            num_issues
        )
        confidence = round(random.uniform(0.65, 0.99), 2)
        
        result = {
            "image_id": image_id,
            "skin_type": skin_type,
            "detected_issues": detected_issues,
            "confidence": confidence
        }
        
        logger.info(f"Analysis complete for {image_id}: {result}")
        return result
