"""
Facial Emotion Detection using Deep Learning
Uses pre-trained models or transfer learning on FER2013 dataset
"""

import cv2
import numpy as np
from tensorflow import keras
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.preprocessing.image import img_to_array
import logging
from typing import Dict, Tuple, Optional
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FacialEmotionDetector:
    """
    CNN-based facial emotion detector using FER2013 emotions.
    
    Emotions: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize facial emotion detector.
        
        Args:
            model_path: Path to pre-trained model weights (if available)
        """
        self.model_path = model_path
        self.model = None
        self.face_cascade = None
        
        # FER2013 emotion labels
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        
        # Image dimensions for FER2013
        self.img_height = 48
        self.img_width = 48
        
        logger.info("Initializing Facial Emotion Detector")
    
    def build_model(self) -> Sequential:
        """
        Build CNN architecture for emotion classification.
        Based on mini-Xception architecture for FER2013.
        
        Returns:
            Compiled Keras Sequential model
        """
        model = Sequential([
            # First convolution block
            Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Second convolution block
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Fully connected layers
            Flatten(),
            Dense(1024, activation='relu'),
            Dropout(0.5),
            Dense(7, activation='softmax')  # 7 emotion classes
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        logger.info("Model architecture built successfully")
        return model
    
    def load_or_build_model(self):
        """
        Load pre-trained model or build new one.
        """
        if self.model_path and os.path.exists(self.model_path):
            try:
                logger.info(f"Loading model from {self.model_path}")
                self.model = load_model(self.model_path)
                logger.info("Pre-trained model loaded successfully")
            except Exception as e:
                logger.warning(f"Could not load model: {e}. Building new model...")
                self.model = self.build_model()
        else:
            logger.info("No pre-trained model found. Building new model...")
            self.model = self.build_model()
            logger.warning("⚠️ Model needs training on FER2013 dataset before use")
    
    def load_face_detector(self):
        """
        Load Haar Cascade for face detection.
        """
        try:
            # Try to load OpenCV's pre-trained face detector
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            if self.face_cascade.empty():
                raise Exception("Failed to load face cascade")
            
            logger.info("Face detector loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading face detector: {e}")
            raise
    
    def initialize(self):
        """
        Initialize both emotion model and face detector.
        """
        self.load_or_build_model()
        self.load_face_detector()
        logger.info("Facial emotion detector initialized")
    
    def preprocess_face(self, face_img: np.ndarray) -> np.ndarray:
        """
        Preprocess face image for model input.
        
        Args:
            face_img: Face image array
            
        Returns:
            Preprocessed image ready for prediction
        """
        # Convert to grayscale if needed
        if len(face_img.shape) == 3:
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        
        # Resize to model input size
        face_img = cv2.resize(face_img, (self.img_width, self.img_height))
        
        # Normalize pixel values
        face_img = face_img.astype('float32') / 255.0
        
        # Reshape for model input
        face_img = img_to_array(face_img)
        face_img = np.expand_dims(face_img, axis=0)
        
        return face_img
    
    def detect_faces(self, image: np.ndarray) -> list:
        """
        Detect faces in image using Haar Cascade.
        
        Args:
            image: Input image array
            
        Returns:
            List of face bounding boxes (x, y, w, h)
        """
        if self.face_cascade is None:
            raise RuntimeError("Face detector not initialized")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        return faces
    
    def predict_emotion(self, face_img: np.ndarray) -> Dict[str, any]:
        """
        Predict emotion from face image.
        
        Args:
            face_img: Face image array
            
        Returns:
            Dictionary with emotion predictions
        """
        if self.model is None:
            raise RuntimeError("Model not initialized")
        
        # Preprocess
        processed = self.preprocess_face(face_img)
        
        # Predict
        predictions = self.model.predict(processed, verbose=0)[0]
        
        # Get top emotion
        max_index = np.argmax(predictions)
        emotion = self.emotion_labels[max_index]
        confidence = float(predictions[max_index])
        
        # Get all emotions with probabilities
        all_emotions = [
            {'emotion': self.emotion_labels[i], 'probability': float(predictions[i])}
            for i in range(len(self.emotion_labels))
        ]
        all_emotions = sorted(all_emotions, key=lambda x: x['probability'], reverse=True)
        
        return {
            'dominant_emotion': emotion,
            'confidence': confidence,
            'all_emotions': all_emotions
        }
    
    def analyze_image(self, image: np.ndarray) -> Dict[str, any]:
        """
        Detect faces and analyze emotions in an image.
        
        Args:
            image: Input image (BGR format from OpenCV)
            
        Returns:
            Dictionary with face locations and emotion predictions
        """
        faces = self.detect_faces(image)
        
        results = []
        for (x, y, w, h) in faces:
            # Extract face ROI
            face_roi = image[y:y+h, x:x+w]
            
            # Predict emotion
            emotion_data = self.predict_emotion(face_roi)
            
            results.append({
                'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)},
                'emotion': emotion_data
            })
        
        return {
            'faces_detected': len(faces),
            'faces': results
        }
    
    def analyze_from_webcam(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Analyze emotion from webcam frame and draw results.
        
        Args:
            frame: Webcam frame (BGR format)
            
        Returns:
            Tuple of (annotated frame, emotion results)
        """
        results = self.analyze_image(frame)
        annotated_frame = frame.copy()
        
        for face_data in results['faces']:
            bbox = face_data['bbox']
            emotion = face_data['emotion']['dominant_emotion']
            confidence = face_data['emotion']['confidence']
            
            # Draw rectangle around face
            cv2.rectangle(
                annotated_frame,
                (bbox['x'], bbox['y']),
                (bbox['x'] + bbox['width'], bbox['y'] + bbox['height']),
                (0, 255, 0),
                2
            )
            
            # Draw emotion label
            label = f"{emotion}: {confidence:.2f}"
            cv2.putText(
                annotated_frame,
                label,
                (bbox['x'], bbox['y'] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
        
        return annotated_frame, results


def map_facial_to_text_emotion(facial_emotion: str) -> str:
    """
    Map facial emotion labels to text emotion labels for consistency.
    
    Args:
        facial_emotion: Emotion from facial detection
        
    Returns:
        Mapped emotion label compatible with text emotion model
    """
    mapping = {
        'Happy': 'joy',
        'Sad': 'sadness',
        'Angry': 'anger',
        'Fear': 'fear',
        'Surprise': 'surprise',
        'Disgust': 'disgust',
        'Neutral': 'neutral'
    }
    
    return mapping.get(facial_emotion, 'neutral')