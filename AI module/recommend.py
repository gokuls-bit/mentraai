"""
Personalized Recommendation System for Mantra AI
Generates motivational and learning feedback based on detected emotions and stress levels
"""

from typing import Dict, List
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmpatheticRecommender:
    """
    Generates personalized recommendations based on emotional state and stress levels.
    """
    
    def __init__(self):
        """Initialize recommender with response templates."""
        self.emotion_responses = self._load_emotion_responses()
        self.learning_strategies = self._load_learning_strategies()
        self.motivational_quotes = self._load_motivational_quotes()
    
    def _load_emotion_responses(self) -> Dict[str, Dict]:
        """
        Load empathetic responses for each emotion.
        
        Returns:
            Dictionary mapping emotions to response templates
        """
        return {
            'joy': {
                'acknowledgment': [
                    "I'm glad to see you're in such a positive mood! 😊",
                    "Your enthusiasm is wonderful! ✨",
                    "Love seeing your positive energy! 🌟"
                ],
                'learning_tip': [
                    "This is a great time to tackle challenging topics!",
                    "Your positive mindset will help you learn faster.",
                    "Channel this energy into creative problem-solving!"
                ],
                'activity': [
                    "Try learning something new and exciting",
                    "Work on a project you're passionate about",
                    "Share your knowledge with others"
                ]
            },
            'sadness': {
                'acknowledgment': [
                    "I notice you might be feeling down. That's okay. 💙",
                    "It's alright to feel sad sometimes. I'm here for you.",
                    "Your feelings are valid. Take your time. 🫂"
                ],
                'learning_tip': [
                    "Start with something simple and rewarding today.",
                    "Small progress is still progress. Be gentle with yourself.",
                    "Focus on topics that usually bring you comfort."
                ],
                'activity': [
                    "Take a break and do something you enjoy",
                    "Connect with a friend or loved one",
                    "Practice self-compassion exercises"
                ]
            },
            'anger': {
                'acknowledgment': [
                    "I sense some frustration. Let's work through this together.",
                    "It's okay to feel angry. Let's channel it productively.",
                    "Your feelings matter. Let's find a constructive outlet."
                ],
                'learning_tip': [
                    "Take a short break before continuing your studies.",
                    "Physical activity might help clear your mind first.",
                    "Break down complex problems into manageable steps."
                ],
                'activity': [
                    "Try a quick breathing exercise (4-7-8 technique)",
                    "Go for a brief walk or do some stretches",
                    "Write down what's bothering you to process it"
                ]
            },
            'fear': {
                'acknowledgment': [
                    "I understand you might be feeling anxious or worried.",
                    "Fear is natural. Let's take this step by step. 🤝",
                    "You're not alone in feeling this way."
                ],
                'learning_tip': [
                    "Start with familiar topics to build confidence.",
                    "Break your goals into very small, achievable steps.",
                    "Remember past challenges you've successfully overcome."
                ],
                'activity': [
                    "Practice grounding techniques (5-4-3-2-1 method)",
                    "List three things you've accomplished recently",
                    "Reach out to your support network"
                ]
            },
            'surprise': {
                'acknowledgment': [
                    "Something unexpected? I'm here to help! ⚡",
                    "Surprises can be great learning opportunities!",
                    "Embrace the unexpected! 🎉"
                ],
                'learning_tip': [
                    "This is perfect for exploring new perspectives!",
                    "Use your curiosity to dive deeper into topics.",
                    "Unexpected moments often lead to breakthroughs."
                ],
                'activity': [
                    "Explore a related topic you haven't considered",
                    "Ask 'why' and 'what if' questions",
                    "Document your discoveries"
                ]
            },
            'love': {
                'acknowledgment': [
                    "Your warmth and positivity shine through! ❤️",
                    "That's beautiful! Love is a powerful motivator.",
                    "Your caring nature is wonderful! 💖"
                ],
                'learning_tip': [
                    "Your passion will fuel deep understanding.",
                    "Connect your learning to what you care about.",
                    "Share your enthusiasm with others!"
                ],
                'activity': [
                    "Mentor someone or share your knowledge",
                    "Create something meaningful",
                    "Express gratitude for your learning journey"
                ]
            },
            'neutral': {
                'acknowledgment': [
                    "You seem calm and centered. Good place to start! 👍",
                    "A neutral state is perfect for focused learning.",
                    "Great mindset for tackling tasks!"
                ],
                'learning_tip': [
                    "This is ideal for complex problem-solving.",
                    "Your focus will serve you well today.",
                    "Maintain this balanced approach."
                ],
                'activity': [
                    "Dive into your most important tasks",
                    "Practice deep work techniques",
                    "Set clear, achievable goals"
                ]
            },
            'disgust': {
                'acknowledgment': [
                    "Something doesn't feel right? Let's address it.",
                    "I understand that reaction. Let's reframe this.",
                    "Your instincts are telling you something."
                ],
                'learning_tip': [
                    "Sometimes resistance reveals important insights.",
                    "Try approaching the topic from a different angle.",
                    "Focus on why this matters in the bigger picture."
                ],
                'activity': [
                    "Take a brief pause to reset",
                    "Find a more engaging resource on the topic",
                    "Connect the material to your interests"
                ]
            }
        }
    
    def _load_learning_strategies(self) -> Dict[str, List[str]]:
        """
        Load learning strategies based on stress and emotional state.
        
        Returns:
            Dictionary of learning strategies
        """
        return {
            'low_stress': [
                "🎯 Set ambitious learning goals for today",
                "📚 Tackle that challenging concept you've been avoiding",
                "🧠 Practice active recall and spaced repetition",
                "🤝 Teach someone else what you're learning",
                "🔬 Experiment with advanced applications"
            ],
            'moderate_stress': [
                "📝 Break your study session into 25-minute intervals (Pomodoro)",
                "🎵 Add background music or white noise if helpful",
                "✅ Focus on one topic at a time",
                "🔄 Review what you already know before new material",
                "💡 Use visual aids and diagrams to simplify concepts"
            ],
            'high_stress': [
                "⏸️ Take a 10-minute break before continuing",
                "🌱 Start with the easiest task to build momentum",
                "📋 Make a simple checklist to reduce overwhelm",
                "🧘 Try a 2-minute mindfulness exercise",
                "👥 Consider studying with a supportive peer"
            ],
            'optimal_flow': [
                "🌊 You're in the flow state - keep going!",
                "⚡ Channel this energy into your most important work",
                "🎨 This is perfect for creative problem-solving",
                "🚀 Push your boundaries while you're in this zone",
                "📈 Build on this momentum for maximum progress"
            ]
        }
    
    def _load_motivational_quotes(self) -> List[str]:
        """
        Load motivational quotes for different situations.
        
        Returns:
            List of motivational quotes
        """
        return [
            "Every expert was once a beginner. Keep going! 💪",
            "Progress, not perfection. You're doing great! 🌟",
            "Your brain is like a muscle - the more you use it, the stronger it gets! 🧠",
            "Mistakes are proof that you're trying. Keep learning! 📚",
            "The only way to do great work is to love what you do. 💙",
            "Small daily improvements lead to stunning results. ✨",
            "You are capable of amazing things! 🌈",
            "Learning is a journey, not a destination. Enjoy the process! 🛤️",
            "Believe in yourself. You've overcome challenges before! 💫",
            "Your potential is limitless. Keep pushing forward! 🚀"
        ]
    
    def generate_response(self, emotion: str, confidence: float, 
                         stress_level: str, mind_score: float = None) -> Dict[str, any]:
        """
        Generate personalized empathetic response.
        
        Args:
            emotion: Detected emotion
            confidence: Confidence of emotion detection
            stress_level: 'low', 'moderate', or 'high'
            mind_score: Optional MindScore value
            
        Returns:
            Dictionary with personalized recommendations
        """
        emotion = emotion.lower()
        
        # Get emotion-specific responses
        emotion_data = self.emotion_responses.get(emotion, self.emotion_responses['neutral'])
        
        # Select responses
        acknowledgment = random.choice(emotion_data['acknowledgment'])
        learning_tip = random.choice(emotion_data['learning_tip'])
        activity = random.choice(emotion_data['activity'])
        
        # Get stress-appropriate learning strategy
        strategy_key = f'{stress_level}_stress' if stress_level != 'optimal' else 'optimal_flow'
        learning_strategies = self.learning_strategies.get(strategy_key, self.learning_strategies['moderate_stress'])
        selected_strategies = random.sample(learning_strategies, min(3, len(learning_strategies)))
        
        # Add motivational quote
        quote = random.choice(self.motivational_quotes)
        
        # Generate study plan recommendation
        study_plan = self._generate_study_plan(emotion, stress_level)
        
        return {
            'acknowledgment': acknowledgment,
            'learning_tip': learning_tip,
            'suggested_activity': activity,
            'learning_strategies': selected_strategies,
            'motivational_quote': quote,
            'study_plan': study_plan,
            'confidence_note': self._get_confidence_note(confidence)
        }
    
    def _generate_study_plan(self, emotion: str, stress_level: str) -> Dict[str, str]:
        """
        Generate personalized study plan based on emotional state.
        
        Args:
            emotion: Current emotion
            stress_level: Current stress level
            
        Returns:
            Dictionary with study plan recommendations
        """
        plans = {
            ('joy', 'low'): {
                'duration': '45-60 minutes',
                'approach': 'Intensive deep work',
                'breaks': 'Every 45 minutes',
                'recommendation': 'Perfect time for challenging material!'
            },
            ('sadness', 'high'): {
                'duration': '15-20 minutes',
                'approach': 'Gentle review of familiar topics',
                'breaks': 'Frequent, every 15 minutes',
                'recommendation': 'Be kind to yourself. Small steps count.'
            },
            ('anger', 'high'): {
                'duration': '10 minutes after calming',
                'approach': 'Physical activity first, then study',
                'breaks': 'Take breaks when needed',
                'recommendation': 'Reset your mind before diving in.'
            },
            ('fear', 'moderate'): {
                'duration': '25-30 minutes',
                'approach': 'Start with confidence-building review',
                'breaks': 'Every 25 minutes',
                'recommendation': 'Build momentum with what you know.'
            }
        }
        
        # Get specific plan or default
        key = (emotion, stress_level)
        if key in plans:
            return plans[key]
        
        # Default moderate plan
        return {
            'duration': '30-40 minutes',
            'approach': 'Balanced focus with regular breaks',
            'breaks': 'Every 30 minutes',
            'recommendation': 'Maintain a steady, sustainable pace.'
        }
    
    def _get_confidence_note(self, confidence: float) -> str:
        """
        Generate note about detection confidence.
        
        Args:
            confidence: Confidence score (0-1)
            
        Returns:
            Human-readable confidence note
        """
        if confidence >= 0.8:
            return "I'm very confident about this assessment."
        elif confidence >= 0.6:
            return "This assessment seems reliable."
        elif confidence >= 0.4:
            return "This is my best estimate - let me know if it feels off."
        else:
            return "I'm somewhat uncertain - please provide more context if needed."
    
    def generate_wellness_recommendations(self, mind_score: float, 
                                         emotion: str, 
                                         stress_level: str) -> List[str]:
        """
        Generate holistic wellness recommendations based on MindScore.
        
        Args:
            mind_score: MindScore value (0-100)
            emotion: Current emotion
            stress_level: Current stress level
            
        Returns:
            List of wellness recommendations
        """
        recommendations = []
        
        # Score-based recommendations
        if mind_score < 40:
            recommendations.extend([
                "🆘 Consider taking a longer break (15-30 minutes)",
                "💬 Reach out to someone you trust",
                "🏥 If feelings persist, consider professional support",
                "🎯 Focus only on essential tasks today"
            ])
        elif mind_score < 60:
            recommendations.extend([
                "🧘 Practice mindfulness or meditation",
                "💪 Light exercise can boost your mood",
                "📱 Limit screen time outside of necessary tasks",
                "😴 Ensure you're getting adequate sleep"
            ])
        else:
            recommendations.extend([
                "🌟 Great mental state! Use it wisely",
                "🎯 This is ideal for tackling big goals",
                "🤝 Help others who might be struggling",
                "📚 Invest in long-term learning projects"
            ])
        
        # Add emotion-specific wellness tips
        emotion_wellness = {
            'sadness': ["🌞 Get some sunlight or bright light exposure", "🎶 Listen to uplifting music"],
            'anger': ["🥊 Try physical exercise to release tension", "📝 Journal your thoughts"],
            'fear': ["🫂 Practice grounding techniques", "📖 Read something comforting"],
            'joy': ["📸 Capture this positive moment", "💝 Spread positivity to others"]
        }
        
        if emotion in emotion_wellness:
            recommendations.extend(emotion_wellness[emotion])
        
        return recommendations[:6]  # Return top 6 recommendations


def get_personalized_feedback(emotion_data: Dict, stress_data: Dict) -> Dict[str, any]:
    """
    Main function to generate complete personalized feedback.
    
    Args:
        emotion_data: Results from emotion detection
        stress_data: Results from stress analysis
        
    Returns:
        Complete personalized feedback package
    """
    recommender = EmpatheticRecommender()
    
    emotion = emotion_data.get('dominant_emotion', 'neutral')
    confidence = emotion_data.get('confidence', 0.0)
    stress_level = stress_data.get('stress_level', 'moderate')
    mind_score = stress_data.get('mind_score', {}).get('mind_score', 50)
    
    # Generate main response
    response = recommender.generate_response(emotion, confidence, stress_level, mind_score)
    
    # Generate wellness recommendations
    wellness_recs = recommender.generate_wellness_recommendations(mind_score, emotion, stress_level)
    
    # Compile complete feedback
    return {
        'empathetic_response': {
            'acknowledgment': response['acknowledgment'],
            'confidence_note': response['confidence_note']
        },
        'learning_guidance': {
            'tip': response['learning_tip'],
            'strategies': response['learning_strategies'],
            'study_plan': response['study_plan']
        },
        'immediate_actions': {
            'suggested_activity': response['suggested_activity'],
            'wellness_recommendations': wellness_recs
        },
        'motivation': {
            'quote': response['motivational_quote'],
            'encouragement': generate_encouragement(mind_score)
        }
    }


def generate_encouragement(mind_score: float) -> str:
    """
    Generate encouraging message based on MindScore.
    
    Args:
        mind_score: MindScore value (0-100)
        
    Returns:
        Encouraging message
    """
    if mind_score >= 80:
        return "You're doing amazingly well! Keep up this fantastic momentum! 🌟"
    elif mind_score >= 60:
        return "You're on a good path! Stay consistent and you'll see great results! 💪"
    elif mind_score >= 40:
        return "You're making progress! Every step forward counts! 🌱"
    else:
        return "Be gentle with yourself. Tomorrow is a new opportunity! 💙"


def get_learning_mode_recommendation(emotion: str, stress_level: str) -> str:
    """
    Recommend optimal learning mode based on emotional state.
    
    Args:
        emotion: Current emotion
        stress_level: Current stress level
        
    Returns:
        Recommended learning mode
    """
    # High energy + low stress = intensive learning
    high_energy_emotions = {'joy', 'surprise', 'love'}
    low_energy_emotions = {'sadness', 'fear'}
    
    if emotion in high_energy_emotions and stress_level == 'low':
        return "🚀 Intensive Mode: Tackle complex problems and new concepts"
    elif emotion in low_energy_emotions or stress_level == 'high':
        return "🌱 Gentle Mode: Review familiar material and consolidate knowledge"
    elif stress_level == 'moderate':
        return "⚖️ Balanced Mode: Mix of review and new learning with breaks"
    else:
        return "📚 Standard Mode: Regular study pace with periodic breaks"