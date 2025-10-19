"""
Text Sentiment Analysis using HuggingFace Transformers
Provides sentiment scores to complement emotion detection
"""

from transformers import pipeline
import torch
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextSentimentAnalyzer:
    """
    Sentiment analysis model for text input.
    Provides positive/negative/neutral sentiment scores.
    """
    
    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"):
        """
        Initialize sentiment analyzer.
        
        Args:
            model_name: HuggingFace model for sentiment analysis
        """
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1
        self.pipeline = None
        
        logger.info(f"Initializing Sentiment Analyzer: {model_name}")
    
    def load_model(self):
        """Load sentiment analysis pipeline."""
        try:
            logger.info("Loading sentiment model...")
            
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                device=self.device,
                top_k=None  # Return all sentiment scores
            )
            
            logger.info("Sentiment model loaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error loading sentiment model: {str(e)}")
            # Fallback to simpler model
            logger.info("Falling back to distilbert sentiment model...")
            self.pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=self.device
            )
            return True
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with sentiment scores
        """
        if self.pipeline is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        if not text or not text.strip():
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'scores': {}
            }
        
        try:
            results = self.pipeline(text)
            
            # Handle different output formats
            if isinstance(results[0], list):
                # Multi-label format
                scores = {item['label']: item['score'] for item in results[0]}
                dominant = max(results[0], key=lambda x: x['score'])
            else:
                # Single label format
                dominant = results[0]
                scores = {dominant['label']: dominant['score']}
            
            return {
                'sentiment': dominant['label'].lower(),
                'confidence': round(dominant['score'], 3),
                'scores': {k: round(v, 3) for k, v in scores.items()}
            }
            
        except Exception as e:
            logger.error(f"Error during sentiment analysis: {str(e)}")
            raise
    
    def get_sentiment_polarity(self, text: str) -> float:
        """
        Get sentiment polarity score (-1 to 1).
        
        Args:
            text: Input text
            
        Returns:
            Polarity score: positive = 1, negative = -1, neutral = 0
        """
        result = self.analyze(text)
        sentiment = result['sentiment']
        confidence = result['confidence']
        
        # Map sentiment to polarity
        if 'positive' in sentiment.lower():
            return confidence
        elif 'negative' in sentiment.lower():
            return -confidence
        else:
            return 0.0


# Global sentiment analyzer instance
_sentiment_analyzer: Optional[TextSentimentAnalyzer] = None


def get_sentiment_analyzer() -> TextSentimentAnalyzer:
    """
    Get or create global sentiment analyzer instance.
    
    Returns:
        Initialized TextSentimentAnalyzer
    """
    global _sentiment_analyzer
    
    if _sentiment_analyzer is None:
        logger.info("Initializing sentiment analyzer...")
        _sentiment_analyzer = TextSentimentAnalyzer()
        _sentiment_analyzer.load_model()
    
    return _sentiment_analyzer


def analyze_sentiment(text: str) -> Dict[str, any]:
    """
    Convenient function to analyze text sentiment.
    
    Args:
        text: Input text
        
    Returns:
        Sentiment analysis results
    """
    analyzer = get_sentiment_analyzer()
    return analyzer.analyze(text)


def combine_emotion_and_sentiment(emotion_data: Dict, sentiment_data: Dict) -> Dict[str, any]:
    """
    Combine emotion and sentiment analysis for richer insights.
    
    Args:
        emotion_data: Results from emotion detection
        sentiment_data: Results from sentiment analysis
        
    Returns:
        Combined analysis
    """
    emotion = emotion_data.get('dominant_emotion', 'neutral')
    emotion_confidence = emotion_data.get('confidence', 0.0)
    
    sentiment = sentiment_data.get('sentiment', 'neutral')
    sentiment_confidence = sentiment_data.get('confidence', 0.0)
    
    # Check for alignment between emotion and sentiment
    positive_emotions = {'joy', 'surprise', 'love'}
    negative_emotions = {'sadness', 'anger', 'fear', 'disgust'}
    
    aligned = False
    if emotion in positive_emotions and 'positive' in sentiment.lower():
        aligned = True
    elif emotion in negative_emotions and 'negative' in sentiment.lower():
        aligned = True
    elif emotion == 'neutral' and 'neutral' in sentiment.lower():
        aligned = True
    
    # Calculate overall mood score
    emotion_valence = emotion_data.get('valence', 0.0)
    sentiment_polarity = 1 if 'positive' in sentiment.lower() else (-1 if 'negative' in sentiment.lower() else 0)
    sentiment_polarity *= sentiment_confidence
    
    overall_mood = (emotion_valence * 0.6 + sentiment_polarity * 0.4)
    
    return {
        'emotion': {
            'label': emotion,
            'confidence': emotion_confidence
        },
        'sentiment': {
            'label': sentiment,
            'confidence': sentiment_confidence
        },
        'aligned': aligned,
        'overall_mood': round(overall_mood, 3),
        'interpretation': interpret_combined_analysis(emotion, sentiment, aligned)
    }


def interpret_combined_analysis(emotion: str, sentiment: str, aligned: bool) -> str:
    """
    Generate human-readable interpretation of combined analysis.
    
    Args:
        emotion: Detected emotion
        sentiment: Detected sentiment
        aligned: Whether emotion and sentiment align
        
    Returns:
        Interpretation string
    """
    if aligned:
        return f"Your {emotion} emotion aligns with {sentiment} sentiment, indicating a clear emotional state."
    else:
        return f"There's a complexity in your emotional state - feeling {emotion} with {sentiment} undertones."
    