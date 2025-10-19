"""
FastAPI Application for Mantra AI - The Empathetic Learning Copilot
Endpoints for emotion detection, stress analysis, and personalized recommendations
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import numpy as np
import cv2
from datetime import datetime
import logging

# Import AI modules
from ai_models.emotion_detection.predict import predict_text_emotion, get_emotion_summary
from ai_models.stress_analysis.predict import predict_stress_level, analyze_text_wellness
from text_sentiment import analyze_sentiment, combine_emotion_and_sentiment
from recommend import get_personalized_feedback, get_learning_mode_recommendation
from emotion_detector import FacialEmotionDetector, map_facial_to_text_emotion

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Mantra AI - Empathetic Learning Copilot",
    description="AI-powered emotion and mental health analysis for personalized learning",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize facial emotion detector (lazy loading)
facial_detector: Optional[FacialEmotionDetector] = None


# ========================
# Pydantic Models
# ========================

class TextAnalysisRequest(BaseModel):
    """Request model for text-based analysis."""
    text: str = Field(..., description="Text input for emotion and stress analysis")
    include_sentiment: bool = Field(default=True, description="Include sentiment analysis")
    include_recommendations: bool = Field(default=True, description="Include personalized recommendations")


class TextAnalysisResponse(BaseModel):
    """Response model for text analysis."""
    timestamp: str
    input_text: str
    emotion_analysis: dict
    stress_analysis: dict
    sentiment_analysis: Optional[dict] = None
    mind_score: dict
    recommendations: Optional[dict] = None
    wellness_summary: str


class EmotionOnlyRequest(BaseModel):
    """Request model for emotion detection only."""
    text: str = Field(..., description="Text to analyze for emotions")


class StressOnlyRequest(BaseModel):
    """Request model for stress analysis only."""
    text: str = Field(..., description="Text to analyze for stress levels")


class MindScoreResponse(BaseModel):
    """Response model for MindScore calculation."""
    mind_score: float
    category: str
    emoji: str
    breakdown: dict


class WellnessTrendRequest(BaseModel):
    """Request model for wellness trend analysis."""
    stress_scores: List[float] = Field(..., description="Historical stress scores")
    emotion_valences: List[float] = Field(..., description="Historical emotion valences")


# ========================
# Health Check
# ========================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Mantra AI - The Empathetic Learning Copilot",
        "status": "active",
        "version": "1.0.0",
        "endpoints": {
            "text_analysis": "/api/v1/analyze/text",
            "emotion_only": "/api/v1/analyze/emotion",
            "stress_only": "/api/v1/analyze/stress",
            "image_analysis": "/api/v1/analyze/image",
            "comprehensive": "/api/v1/analyze/comprehensive"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# ========================
# Text Analysis Endpoints
# ========================

@app.post("/api/v1/analyze/emotion", tags=["Text Analysis"])
async def analyze_emotion_only(request: EmotionOnlyRequest):
    """
    Analyze emotion from text input only.
    
    Returns emotion detection results without stress analysis.
    """
    try:
        logger.info(f"Emotion analysis request: {request.text[:50]}...")
        
        result = predict_text_emotion(request.text)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "emotion_analysis": result,
            "summary": get_emotion_summary(request.text)
        }
        
    except Exception as e:
        logger.error(f"Error in emotion analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/v1/analyze/stress", tags=["Text Analysis"])
async def analyze_stress_only(request: StressOnlyRequest):
    """
    Analyze stress level from text input only.
    
    Returns stress detection results without emotion analysis.
    """
    try:
        logger.info(f"Stress analysis request: {request.text[:50]}...")
        
        result = predict_stress_level(request.text)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "stress_analysis": result
        }
        
    except Exception as e:
        logger.error(f"Error in stress analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/v1/analyze/text", response_model=TextAnalysisResponse, tags=["Text Analysis"])
async def analyze_text(request: TextAnalysisRequest):
    """
    Comprehensive text analysis including emotion, stress, and recommendations.
    
    This is the main endpoint for text-based mental health analysis.
    Returns MindScore and personalized learning recommendations.
    """
    try:
        logger.info(f"Comprehensive text analysis: {request.text[:50]}...")
        
        # Get comprehensive wellness analysis
        result = analyze_text_wellness(request.text)
        
        # Add sentiment analysis if requested
        if request.include_sentiment:
            sentiment = analyze_sentiment(request.text)
            combined = combine_emotion_and_sentiment(
                result['emotion_analysis'],
                sentiment
            )
            result['sentiment_analysis'] = sentiment
            result['combined_analysis'] = combined
        
        # Add recommendations if requested
        if request.include_recommendations:
            recommendations = get_personalized_feedback(
                result['emotion_analysis'],
                result['stress_analysis']
            )
            result['recommendations'] = recommendations
            
            # Add learning mode recommendation
            result['learning_mode'] = get_learning_mode_recommendation(
                result['emotion_analysis']['dominant_emotion'],
                result['stress_analysis']['stress_level']
            )
        
        # Add timestamp
        result['timestamp'] = datetime.utcnow().isoformat()
        
        return result
        
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# ========================
# Image Analysis Endpoints
# ========================

@app.post("/api/v1/analyze/image", tags=["Image Analysis"])
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze emotion from uploaded image (facial expression).
    
    Detects faces and predicts emotions from facial expressions.
    """
    try:
        logger.info(f"Image analysis request: {file.filename}")
        
        # Initialize facial detector if needed
        global facial_detector
        if facial_detector is None:
            facial_detector = FacialEmotionDetector()
            facial_detector.initialize()
        
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Analyze image
        result = facial_detector.analyze_image(image)
        
        # Map facial emotions to text emotions for consistency
        for face in result['faces']:
            facial_emotion = face['emotion']['dominant_emotion']
            face['emotion']['mapped_emotion'] = map_facial_to_text_emotion(facial_emotion)
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "filename": file.filename,
            "analysis": result
        }
        
    except Exception as e:
        logger.error(f"Error in image analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# ========================
# Comprehensive Analysis
# ========================

@app.post("/api/v1/analyze/comprehensive", tags=["Comprehensive Analysis"])
async def comprehensive_analysis(
    text: Optional[str] = None,
    image: Optional[UploadFile] = File(None)
):
    """
    Comprehensive analysis combining text and image inputs.
    
    Analyzes both text (if provided) and facial expressions (if image provided)
    to create a complete emotional and mental health profile.
    """
    try:
        logger.info("Comprehensive multimodal analysis request")
        
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "text_analysis": None,
            "image_analysis": None,
            "combined_insights": None
        }
        
        # Analyze text if provided
        if text:
            text_result = analyze_text_wellness(text)
            results['text_analysis'] = text_result
        
        # Analyze image if provided
        if image:
            global facial_detector
            if facial_detector is None:
                facial_detector = FacialEmotionDetector()
                facial_detector.initialize()
            
            contents = await image.read()
            nparr = np.frombuffer(contents, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is not None:
                image_result = facial_detector.analyze_image(img)
                results['image_analysis'] = image_result
        
        # Generate combined insights if both available
        if results['text_analysis'] and results['image_analysis']:
            if results['image_analysis']['faces_detected'] > 0:
                facial_emotion = results['image_analysis']['faces'][0]['emotion']['dominant_emotion']
                text_emotion = results['text_analysis']['emotion_analysis']['dominant_emotion']
                
                alignment = "aligned" if facial_emotion.lower() == text_emotion.lower() else "misaligned"
                
                results['combined_insights'] = {
                    "alignment": alignment,
                    "interpretation": f"Facial expression shows {facial_emotion} while text conveys {text_emotion}. "
                                    f"This {'confirms' if alignment == 'aligned' else 'suggests complexity in'} your emotional state."
                }
        
        # Add recommendations based on available data
        if results['text_analysis']:
            recommendations = get_personalized_feedback(
                results['text_analysis']['emotion_analysis'],
                results['text_analysis']['stress_analysis']
            )
            results['recommendations'] = recommendations
        
        return results
        
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# ========================
# Utility Endpoints
# ========================

@app.get("/api/v1/emotions/list", tags=["Utilities"])
async def list_emotions():
    """Get list of supported emotions."""
    return {
        "text_emotions": ["joy", "sadness", "anger", "fear", "surprise", "love", "disgust", "neutral"],
        "facial_emotions": ["Happy", "Sad", "Angry", "Fear", "Surprise", "Disgust", "Neutral"]
    }


@app.get("/api/v1/stress/levels", tags=["Utilities"])
async def list_stress_levels():
    """Get information about stress levels."""
    return {
        "levels": {
            "low": {
                "range": "0.0 - 0.33",
                "description": "Calm and relaxed state"
            },
            "moderate": {
                "range": "0.34 - 0.66",
                "description": "Some stress indicators present"
            },
            "high": {
                "range": "0.67 - 1.0",
                "description": "Significant stress markers detected"
            }
        }
    }


# ========================
# Model Management
# ========================

@app.post("/api/v1/models/preload", tags=["Model Management"])
async def preload_models():
    """
    Preload all AI models to reduce first-request latency.
    Useful for production deployment.
    """
    try:
        logger.info("Preloading all models...")
        
        # Preload text emotion model
        from ai_models.emotion_detection.predict import get_model as get_emotion_model
        emotion_model = get_emotion_model()
        
        # Preload stress analysis model
        from ai_models.stress_analysis.predict import get_model as get_stress_model
        stress_model = get_stress_model()
        
        # Preload sentiment model
        from text_sentiment import get_sentiment_analyzer
        sentiment_model = get_sentiment_analyzer()
        
        logger.info("All models preloaded successfully")
        
        return {
            "status": "success",
            "message": "All models preloaded",
            "models": ["emotion_detection", "stress_analysis", "sentiment_analysis"]
        }
        
    except Exception as e:
        logger.error(f"Error preloading models: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Model preloading failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)