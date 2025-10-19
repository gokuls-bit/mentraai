"""
Example usage of Mantra AI - The Empathetic Learning Copilot
Demonstrates all major features and API endpoints
"""

import requests
import json
from typing import Dict
import time


class MantraAIClient:
    """Client for interacting with Mantra AI API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize Mantra AI client.
        
        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def analyze_text(self, text: str, include_sentiment: bool = True, 
                    include_recommendations: bool = True) -> Dict:
        """
        Comprehensive text analysis.
        
        Args:
            text: Input text to analyze
            include_sentiment: Include sentiment analysis
            include_recommendations: Include recommendations
            
        Returns:
            Complete analysis results
        """
        endpoint = f"{self.base_url}/api/v1/analyze/text"
        payload = {
            "text": text,
            "include_sentiment": include_sentiment,
            "include_recommendations": include_recommendations
        }
        
        response = self.session.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    
    def analyze_emotion(self, text: str) -> Dict:
        """Analyze emotion only."""
        endpoint = f"{self.base_url}/api/v1/analyze/emotion"
        response = self.session.post(endpoint, json={"text": text})
        response.raise_for_status()
        return response.json()
    
    def analyze_stress(self, text: str) -> Dict:
        """Analyze stress only."""
        endpoint = f"{self.base_url}/api/v1/analyze/stress"
        response = self.session.post(endpoint, json={"text": text})
        response.raise_for_status()
        return response.json()
    
    def analyze_image(self, image_path: str) -> Dict:
        """Analyze facial emotion from image."""
        endpoint = f"{self.base_url}/api/v1/analyze/image"
        
        with open(image_path, 'rb') as img_file:
            files = {'file': img_file}
            response = self.session.post(endpoint, files=files)
            response.raise_for_status()
            return response.json()
    
    def comprehensive_analysis(self, text: str = None, image_path: str = None) -> Dict:
        """Multimodal analysis combining text and image."""
        endpoint = f"{self.base_url}/api/v1/analyze/comprehensive"
        
        data = {}
        files = {}
        
        if text:
            data['text'] = text
        
        if image_path:
            files['image'] = open(image_path, 'rb')
        
        response = self.session.post(endpoint, data=data, files=files)
        
        if image_path:
            files['image'].close()
        
        response.raise_for_status()
        return response.json()
    
    def preload_models(self) -> Dict:
        """Preload all models for faster inference."""
        endpoint = f"{self.base_url}/api/v1/models/preload"
        response = self.session.post(endpoint)
        response.raise_for_status()
        return response.json()


def print_section(title: str):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def print_results(results: Dict, indent: int = 0):
    """Pretty print results."""
    spacing = "  " * indent
    
    for key, value in results.items():
        if isinstance(value, dict):
            print(f"{spacing}{key}:")
            print_results(value, indent + 1)
        elif isinstance(value, list):
            print(f"{spacing}{key}:")
            for item in value:
                if isinstance(item, dict):
                    print_results(item, indent + 1)
                else:
                    print(f"{spacing}  - {item}")
        else:
            print(f"{spacing}{key}: {value}")


def example_1_basic_emotion_detection():
    """Example 1: Basic emotion detection from text."""
    print_section("Example 1: Basic Emotion Detection")
    
    client = MantraAIClient()
    
    test_texts = [
        "I'm so excited about learning Python! This is amazing!",
        "I feel so overwhelmed with all these assignments.",
        "Why is this concept so difficult to understand? I'm frustrated.",
        "I'm worried I won't pass the exam next week."
    ]
    
    for text in test_texts:
        print(f"Input: '{text}'")
        result = client.analyze_emotion(text)
        
        emotion_data = result['emotion_analysis']
        print(f"  Emotion: {emotion_data['dominant_emotion'].upper()}")
        print(f"  Confidence: {emotion_data['confidence']:.1%}")
        print(f"  Valence: {emotion_data['valence']:.2f}")
        print()


def example_2_stress_analysis():
    """Example 2: Stress level analysis."""
    print_section("Example 2: Stress Level Analysis")
    
    client = MantraAIClient()
    
    stress_scenarios = [
        "Everything is going great! I feel calm and in control.",
        "There's a lot to do but I think I can manage it.",
        "I'm so stressed! Deadlines everywhere and I can't focus!"
    ]
    
    for text in stress_scenarios:
        print(f"Input: '{text}'")
        result = client.analyze_stress(text)
        
        stress_data = result['stress_analysis']
        print(f"  Stress Level: {stress_data['stress_level'].upper()}")
        print(f"  Stress Score: {stress_data['stress_score']:.1%}")
        print(f"  Description: {stress_data['description']}")
        print(f"  Recommendations:")
        for rec in stress_data.get('recommendations', [])[:3]:
            print(f"    • {rec}")
        print()


def example_3_comprehensive_analysis():
    """Example 3: Comprehensive wellness analysis."""
    print_section("Example 3: Comprehensive Wellness Analysis with MindScore")
    
    client = MantraAIClient()
    
    text = """
    I've been studying for hours and I'm exhausted. 
    There's so much material to cover and I feel like I'm not making progress.
    Sometimes I wonder if I'm smart enough for this course.
    """
    
    print(f"Student Journal Entry:\n{text}\n")
    
    result = client.analyze_text(text, include_recommendations=True)
    
    # Display MindScore
    mind_score = result['mind_score']
    print(f"🎯 MindScore: {mind_score['mind_score']:.1f}/100 {mind_score['emoji']}")
    print(f"   Category: {mind_score['category']}")
    print(f"   Breakdown:")
    print(f"     - Emotion: {mind_score['breakdown']['emotion_contribution']:.1f}")
    print(f"     - Stress: {mind_score['breakdown']['stress_contribution']:.1f}")
    
    # Display emotion analysis
    print(f"\n😊 Emotion Analysis:")
    emotion = result['emotion_analysis']
    print(f"   Dominant: {emotion['dominant_emotion'].upper()} ({emotion['confidence']:.1%})")
    print(f"   Top 3 Emotions:")
    for e in emotion['all_emotions'][:3]:
        print(f"     • {e['emotion']}: {e['score']:.1%}")
    
    # Display stress analysis
    print(f"\n😰 Stress Analysis:")
    stress = result['stress_analysis']
    print(f"   Level: {stress['stress_level'].upper()} ({stress['stress_score']:.1%})")
    print(f"   Description: {stress['description']}")
    
    # Display recommendations
    if 'recommendations' in result:
        print(f"\n💡 Personalized Recommendations:")
        recs = result['recommendations']
        
        print(f"\n   Empathetic Response:")
        print(f"     {recs['empathetic_response']['acknowledgment']}")
        
        print(f"\n   Learning Guidance:")
        print(f"     {recs['learning_guidance']['tip']}")
        
        print(f"\n   Immediate Actions:")
        print(f"     • {recs['immediate_actions']['suggested_activity']}")
        
        print(f"\n   Study Plan:")
        plan = recs['learning_guidance']['study_plan']
        print(f"     Duration: {plan['duration']}")
        print(f"     Approach: {plan['approach']}")
        print(f"     Recommendation: {plan['recommendation']}")
        
        print(f"\n   Motivation:")
        print(f"     {recs['motivation']['quote']}")
    
    print(f"\n📝 Wellness Summary:")
    print(f"   {result['wellness_summary']}")


def example_4_learning_mode_recommendation():
    """Example 4: Get learning mode recommendations."""
    print_section("Example 4: Adaptive Learning Mode")
    
    client = MantraAIClient()
    
    scenarios = [
        ("I'm feeling great today! Let's tackle something challenging!", "Optimal State"),
        ("I'm a bit tired but want to review what I learned.", "Low Energy"),
        ("Feeling confident and ready to learn!", "High Motivation")
    ]
    
    for text, scenario in scenarios:
        print(f"Scenario: {scenario}")
        print(f"Student says: '{text}'")
        
        result = client.analyze_text(text)
        
        if 'learning_mode' in result:
            print(f"  Recommended Mode: {result['learning_mode']}")
        
        emotion = result['emotion_analysis']['dominant_emotion']
        stress = result['stress_analysis']['stress_level']
        mind_score = result['mind_score']['mind_score']
        
        print(f"  Emotion: {emotion}, Stress: {stress}, MindScore: {mind_score:.0f}/100")
        print()


def example_5_batch_processing():
    """Example 5: Batch processing multiple inputs."""
    print_section("Example 5: Batch Processing Student Check-ins")
    
    client = MantraAIClient()
    
    student_checkins = {
        "Student A": "I'm loving this course! Everything makes sense now.",
        "Student B": "I'm confused about the last topic. Need help.",
        "Student C": "Stressed about the upcoming test. So much to remember.",
        "Student D": "Taking a break. Feeling good about my progress.",
        "Student E": "I hate this assignment. It's too difficult and boring."
    }
    
    results = []
    
    for student, checkin in student_checkins.items():
        result = client.analyze_text(checkin, include_recommendations=False)
        results.append({
            'student': student,
            'text': checkin,
            'emotion': result['emotion_analysis']['dominant_emotion'],
            'stress': result['stress_analysis']['stress_level'],
            'mind_score': result['mind_score']['mind_score']
        })
    
    # Display summary
    print("Class Wellness Dashboard:")
    print(f"{'Student':<12} {'MindScore':<12} {'Emotion':<12} {'Stress':<12}")
    print("-" * 50)
    
    for r in results:
        score_emoji = "🟢" if r['mind_score'] >= 70 else "🟡" if r['mind_score'] >= 40 else "🔴"
        print(f"{r['student']:<12} {score_emoji} {r['mind_score']:>5.0f}/100   {r['emotion']:<12} {r['stress']:<12}")
    
    # Identify at-risk students
    at_risk = [r for r in results if r['mind_score'] < 40]
    if at_risk:
        print(f"\n⚠️  At-Risk Students Requiring Attention: {len(at_risk)}")
        for student in at_risk:
            print(f"   • {student['student']}: MindScore {student['mind_score']:.0f}")


def example_6_trend_analysis():
    """Example 6: Wellness trend over time."""
    print_section("Example 6: Student Wellness Trend Analysis")
    
    client = MantraAIClient()
    
    # Simulate student check-ins over time
    weekly_checkins = [
        "Week 1: Excited to start! Everything is new and interesting.",
        "Week 2: Still motivated but starting to feel the workload.",
        "Week 3: Midterms approaching. Feeling stressed and tired.",
        "Week 4: Exam done! Feeling relieved but exhausted.",
        "Week 5: Back on track. Managing better now."
    ]
    
    mind_scores = []
    stress_scores = []
    
    print("Student Weekly Check-ins:\n")
    
    for checkin in weekly_checkins:
        result = client.analyze_text(checkin, include_recommendations=False)
        mind_score = result['mind_score']['mind_score']
        stress_score = result['stress_analysis']['stress_score']
        
        mind_scores.append(mind_score)
        stress_scores.append(stress_score)
        
        print(f"{checkin}")
        print(f"  MindScore: {mind_score:.0f}/100, Stress: {stress_score:.1%}\n")
    
    # Analyze trend
    print("Trend Analysis:")
    avg_mind_score = sum(mind_scores) / len(mind_scores)
    print(f"  Average MindScore: {avg_mind_score:.1f}/100")
    
    # Check if improving or declining
    recent_avg = sum(mind_scores[-2:]) / 2
    early_avg = sum(mind_scores[:2]) / 2
    
    if recent_avg > early_avg + 10:
        print(f"  Trend: ✅ IMPROVING (recent: {recent_avg:.0f} vs early: {early_avg:.0f})")
    elif recent_avg < early_avg - 10:
        print(f"  Trend: ⚠️ DECLINING (recent: {recent_avg:.0f} vs early: {early_avg:.0f})")
    else:
        print(f"  Trend: ➡️ STABLE")


def example_7_performance_test():
    """Example 7: Test API performance."""
    print_section("Example 7: Performance Testing")
    
    client = MantraAIClient()
    
    # Preload models
    print("Preloading models...")
    client.preload_models()
    print("✅ Models preloaded\n")
    
    test_text = "I'm working on a challenging project and feeling motivated!"
    num_requests = 10
    
    print(f"Running {num_requests} sequential requests...\n")
    
    times = []
    for i in range(num_requests):
        start = time.time()
        result = client.analyze_text(test_text, include_recommendations=False)
        elapsed = time.time() - start
        times.append(elapsed)
        
        print(f"Request {i+1}: {elapsed*1000:.0f}ms")
    
    print(f"\nPerformance Summary:")
    print(f"  Average: {sum(times)/len(times)*1000:.0f}ms")
    print(f"  Min: {min(times)*1000:.0f}ms")
    print(f"  Max: {max(times)*1000:.0f}ms")


def main():
    """Run all examples."""
    print("\n" + "🧠"*35)
    print("  MANTRA AI - THE EMPATHETIC LEARNING COPILOT")
    print("  Complete Usage Examples")
    print("🧠"*35)
    
    try:
        # Check if API is running
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code != 200:
            print("\n❌ Error: API is not responding properly")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API. Make sure it's running on http://localhost:8000")
        print("   Start the API with: python main.py")
        return
    
    # Run examples
    example_1_basic_emotion_detection()
    example_2_stress_analysis()
    example_3_comprehensive_analysis()
    example_4_learning_mode_recommendation()
    example_5_batch_processing()
    example_6_trend_analysis()
    example_7_performance_test()
    
    print("\n" + "="*70)
    print("  ✅ All examples completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()