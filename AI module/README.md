# Mantra AI - The Empathetic Learning Copilot 🧠💙

An AI-powered emotion and mental health analysis system designed to provide personalized learning recommendations based on emotional state and stress levels.

## 🌟 Features

- **Text Emotion Detection**: Analyze emotions from text using state-of-the-art transformer models
- **Facial Emotion Recognition**: Detect emotions from webcam/images using CNN-based deep learning
- **Stress Level Analysis**: Comprehensive stress detection from text patterns and sentiment
- **MindScore™**: Holistic mental wellness metric (0-100) combining emotion and stress analysis
- **Personalized Recommendations**: Context-aware learning strategies and wellness suggestions
- **RESTful API**: FastAPI-based endpoints for easy integration

## 📁 Project Structure

```
mantra-ai/
│
├── ai_models/
│   ├── __init__.py
│   ├── emotion_detection/
│   │   ├── model.py           # HuggingFace emotion classifier
│   │   ├── preprocess.py      # Text preprocessing utilities
│   │   └── predict.py         # Emotion prediction functions
│   │
│   └── stress_analysis/
│       ├── model.py           # Stress detection model
│       ├── utils.py           # MindScore calculation & utilities
│       └── predict.py         # Stress prediction functions
│
├── emotion_detector.py        # Facial emotion detection (CNN/Transfer Learning)
├── text_sentiment.py          # Sentiment analysis module
├── recommend.py               # Personalized recommendation engine
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mantra-ai.git
cd mantra-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the API

```bash
# Start the FastAPI server
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API documentation (Swagger): `http://localhost:8000/docs`

## 📚 API Endpoints

### Health Check
```http
GET /
GET /health
```

### Text Analysis

#### 1. Comprehensive Text Analysis
```http
POST /api/v1/analyze/text
Content-Type: application/json

{
  "text": "I'm feeling overwhelmed with all the assignments due this week",
  "include_sentiment": true,
  "include_recommendations": true
}
```

**Response:**
```json
{
  "timestamp": "2025-10-19T10:30:00Z",
  "emotion_analysis": {
    "dominant_emotion": "fear",
    "confidence": 0.78,
    "valence": -0.23
  },
  "stress_analysis": {
    "stress_score": 0.72,
    "stress_level": "high"
  },
  "mind_score": {
    "mind_score": 35.5,
    "category": "Poor",
    "emoji": "😔"
  },
  "recommendations": {
    "empathetic_response": {
      "acknowledgment": "I understand you might be feeling anxious or worried."
    },
    "learning_guidance": {
      "strategies": ["Take a 10-minute break", "Break tasks into small steps"]
    }
  }
}
```

#### 2. Emotion Detection Only
```http
POST /api/v1/analyze/emotion

{
  "text": "I'm so excited about this new project!"
}
```

#### 3. Stress Analysis Only
```http
POST /api/v1/analyze/stress

{
  "text": "Deadline approaching, feeling pressure"
}
```

### Image Analysis

#### Facial Emotion Detection
```http
POST /api/v1/analyze/image
Content-Type: multipart/form-data

file: [image file]
```

### Comprehensive Multimodal Analysis
```http
POST /api/v1/analyze/comprehensive
Content-Type: multipart/form-data

text: "Feeling nervous about the presentation"
image: [webcam capture or image file]
```

### Utility Endpoints

```http
GET /api/v1/emotions/list        # List supported emotions
GET /api/v1/stress/levels         # Stress level information
POST /api/v1/models/preload       # Preload models for faster inference
```

## 🧠 AI Models Used

### Text Emotion Detection
- **Model**: `j-hartmann/emotion-english-distilroberta-base`
- **Emotions**: joy, sadness, anger, fear, surprise, love, disgust, neutral
- **Architecture**: DistilRoBERTa (transformer-based)

### Sentiment Analysis
- **Model**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Output**: positive, negative, neutral with confidence scores

### Facial Emotion Detection
- **Dataset**: FER2013
- **Architecture**: Mini-Xception CNN
- **Emotions**: Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral
- **Input**: 48x48 grayscale images

### Stress Analysis
- **Approach**: Multi-component analysis
  - Sentiment-based stress indicators (40%)
  - Keyword detection (40%)
  - Linguistic features (20%)

## 💯 MindScore™ Calculation

MindScore is a holistic mental wellness metric (0-100) calculated as:

```
MindScore = (Emotion_Component × 0.5) + (Stress_Component × 0.5)

Where:
- Emotion_Component = normalized emotional valence (0-100)
- Stress_Component = inverted stress score (0-100, lower stress = higher score)
```

### Score Categories:
- **80-100**: Excellent 🌟 - Optimal mental state
- **60-79**: Good 😊 - Positive mental state
- **40-59**: Fair 😐 - Manageable stress
- **20-39**: Poor 😔 - Significant stress
- **0-19**: Critical 😰 - Requires attention

## 🎯 Use Cases

### 1. Learning Platforms
```python
# Student submits learning reflection
response = analyze_text({
    "text": student_journal_entry,
    "include_recommendations": True
})

# Adjust learning content based on MindScore
if response['mind_score']['mind_score'] < 40:
    # Provide easier, confidence-building content
    adjust_difficulty(student_id, difficulty='easy')
```

### 2. Mental Health Monitoring
```python
# Track student wellness over time
daily_checkin = analyze_text_wellness(checkin_text)
store_mind_score(student_id, daily_checkin['mind_score'])

# Alert if concerning trends detected
if detect_declining_trend(student_id):
    notify_counselor(student_id)
```

### 3. Adaptive Learning Systems
```python
# Real-time emotion detection during study session
emotion_result = predict_text_emotion(chat_message)

if emotion_result['dominant_emotion'] == 'frustration':
    # Provide hints or alternative explanations
    offer_assistance(student_id)
```

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Model Paths (if using local models)
EMOTION_MODEL_PATH=/path/to/emotion/model
FACIAL_MODEL_PATH=/path/to/facial/model.h5

# Logging
LOG_LEVEL=INFO
```

### Model Training (Optional)

To train the facial emotion detector on FER2013:

```python
from emotion_detector import FacialEmotionDetector

# Initialize detector
detector = FacialEmotionDetector()
detector.load_or_build_model()

# Train on FER2013 dataset (download separately)
# Dataset: https://www.kaggle.com/datasets/msambare/fer2013
history = detector.model.fit(
    train_data,
    validation_data=val_data,
    epochs=50,
    batch_size=32
)

# Save trained model
detector.model.save('models/facial_emotion_model.h5')
```

## 📊 Example Workflows

### Complete Wellness Check

```python
import requests

# Analyze text input
response = requests.post(
    'http://localhost:8000/api/v1/analyze/text',
    json={
        'text': 'I have so much to study but I keep procrastinating',
        'include_sentiment': True,
        'include_recommendations': True
    }
)

result = response.json()

print(f"MindScore: {result['mind_score']['mind_score']}/100")
print(f"Emotion: {result['emotion_analysis']['dominant_emotion']}")
print(f"Stress: {result['stress_analysis']['stress_level']}")
print(f"\nRecommendations:")
for rec in result['recommendations']['immediate_actions']['wellness_recommendations']:
    print(f"  {rec}")
```

### Multimodal Analysis

```python
# Combine text and image analysis
with open('webcam_capture.jpg', 'rb') as img:
    response = requests.post(
        'http://localhost:8000/api/v1/analyze/comprehensive',
        data={'text': 'Feeling stressed about exams'},
        files={'image': img}
    )

result = response.json()

# Check emotion alignment
if result['combined_insights']['alignment'] == 'misaligned':
    print("⚠️ Your words and expressions don't match - there might be hidden emotions")
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test specific endpoint
pytest tests/test_emotion_detection.py -v

# With coverage
pytest --cov=ai_models tests/
```

### Example Test

```python
import pytest
from ai_models.emotion_detection.predict import predict_text_emotion

def test_emotion_detection():
    result = predict_text_emotion("I am so happy today!")
    assert result['dominant_emotion'] == 'joy'
    assert result['confidence'] > 0.6

def test_stress_analysis():
    from ai_models.stress_analysis.predict import predict_stress_level
    result = predict_stress_level("Everything is overwhelming")
    assert result['stress_level'] in ['moderate', 'high']
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Preload models
RUN python -c "from ai_models.emotion_detection.predict import get_model; get_model()"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t mantra-ai .
docker run -p 8000:8000 mantra-ai
```

### Production Considerations

1. **Model Caching**: Preload models at startup
```python
@app.on_event("startup")
async def startup_event():
    await preload_models()
```

2. **Rate Limiting**: Implement API rate limits
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/analyze/text")
@limiter.limit("10/minute")
async def analyze_text(request: Request, data: TextAnalysisRequest):
    ...
```

3. **Async Processing**: Use background tasks for heavy operations
```python
from fastapi import BackgroundTasks

@app.post("/api/v1/analyze/batch")
async def batch_analysis(texts: List[str], background_tasks: BackgroundTasks):
    background_tasks.add_task(process_batch, texts)
    return {"status": "processing"}
```

## 📈 Performance Metrics

### Inference Speed (CPU)
- Text emotion detection: ~100-200ms
- Stress analysis: ~150-250ms
- Facial emotion detection: ~50-100ms per face
- Complete analysis: ~300-500ms

### Model Sizes
- Text emotion model: ~500MB
- Sentiment model: ~300MB
- Facial emotion model: ~5MB (after training)

## 🔐 Privacy & Ethics

- **Data Privacy**: No data is stored by default
- **Consent**: Always obtain user consent for emotion tracking
- **Transparency**: Inform users about AI analysis
- **Limitations**: AI predictions are not clinical diagnoses
- **Human Oversight**: Critical decisions should involve human review

## 🤝 Contributing

Contributions welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- HuggingFace for transformer models
- FER2013 dataset contributors
- FastAPI framework
- OpenCV community

## 📞 Support

For issues, questions, or contributions:
- GitHub Issues: [your-repo/issues]
- Email: support@mantraai.com
- Documentation: [your-docs-site]

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Voice emotion detection
- [ ] Integration with popular LMS platforms
- [ ] Mobile SDK (iOS/Android)
- [ ] Advanced stress prediction models
- [ ] Personalized intervention recommendations
- [ ] Long-term wellness trend analysis
- [ ] Group wellness analytics for educators

---

Built with ❤️ for empathetic learning

**Version**: 1.0.0  
**Last Updated**: October 2025