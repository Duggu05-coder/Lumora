import streamlit as st
import pandas as pd
from datetime import datetime
import json

from therapy_bot import TherapyBot
from emotion_tracker import EmotionTracker
from breathing_exercises import BreathingExercises
from camera_analysis import CameraAnalysis
from daily_challenges import DailyChallenges
from data_manager import DataManager
from meditation_module import MeditationModule
from quick_remedies import QuickRemedies
from translations import get_text, LANGUAGES
import random

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.language = 'en'
    st.session_state.chat_history = []
    st.session_state.emotion_history = []
    st.session_state.current_emotion = 5
    st.session_state.therapy_bot = TherapyBot()
    st.session_state.emotion_tracker = EmotionTracker()
    st.session_state.breathing_exercises = BreathingExercises()
    st.session_state.camera_analysis = CameraAnalysis()
    st.session_state.meditation_module = MeditationModule()
    st.session_state.daily_challenges = DailyChallenges()
    st.session_state.data_manager = DataManager()
    st.session_state.quick_remedies = QuickRemedies()

def get_current_detected_emotion():
    """Get the current detected emotion from chat analysis or camera."""
    # Check for recent camera emotion detection
    if len(st.session_state.camera_analysis.emotion_data) > 0:
        latest_camera = st.session_state.camera_analysis.emotion_data[-1]
        # Convert camera emotion to 1-10 scale
        camera_emotion = convert_camera_emotion_to_scale(latest_camera['primary_emotion'])
        return camera_emotion
    
    # Check for recent chat-based emotion detection
    if hasattr(st.session_state, 'last_chat_emotion') and st.session_state.last_chat_emotion:
        return st.session_state.last_chat_emotion
    
    return None

def convert_camera_emotion_to_scale(emotion_name: str) -> int:
    """Convert camera emotion name to 1-10 scale with enhanced mapping."""
    emotion_mapping = {
        'angry': 2,
        'rage': 1,
        'furious': 1,
        'disgust': 2, 
        'fear': 2,
        'terror': 1,
        'panic': 1,
        'sad': 1,
        'depressed': 1,
        'devastated': 1,
        'trauma': 1,
        'shock': 2,
        'surprise': 6,
        'confused': 4,
        'neutral': 5,
        'calm': 6,
        'content': 7,
        'happy': 8,
        'joy': 9,
        'ecstatic': 10,
        'peaceful': 7
    }
    return emotion_mapping.get(emotion_name.lower(), 5)

def detect_emotion_from_text(text: str) -> int:
    """Enhanced text-based emotion detection including anger and trauma."""
    text_lower = text.lower()
    
    # Very negative emotions (1-2) - Trauma and severe distress
    trauma_words = ['traumatized', 'ptsd', 'flashback', 'nightmare', 'panic attack', 'breakdown', 'suicidal', 'self-harm', 'abuse', 'violated', 'betrayed', 'shattered', 'broken inside']
    if any(word in text_lower for word in trauma_words):
        return 1
    
    very_sad_words = ['terrible', 'awful', 'hopeless', 'devastated', 'miserable', 'depressed', 'worthless', 'empty', 'numb', 'lost']
    if any(word in text_lower for word in very_sad_words):
        return 1
    
    # Anger expressions (2-3)
    anger_words = ['angry', 'furious', 'rage', 'mad', 'pissed', 'enraged', 'livid', 'outraged', 'hate', 'disgusted', 'annoyed', 'irritated']
    if any(word in text_lower for word in anger_words):
        return 2
    
    sad_words = ['sad', 'upset', 'down', 'bad', 'frustrated', 'worried', 'anxious', 'scared', 'hurt', 'disappointed']
    if any(word in text_lower for word in sad_words):
        return 2
    
    # Neutral-low emotions (3-4)  
    low_words = ['tired', 'bored', 'stressed', 'overwhelmed', 'confused', 'uncertain', 'empty', 'disconnected']
    if any(word in text_lower for word in low_words):
        return 3
    
    # Neutral emotions (5)
    neutral_words = ['okay', 'fine', 'meh', 'whatever', 'normal', 'average', 'nothing', 'same', 'usual', 'alright']
    if any(word in text_lower for word in neutral_words):
        return 5
    
    # Positive emotions (6-10)
    happy_words = ['good', 'great', 'happy', 'excited', 'amazing', 'wonderful', 'fantastic', 'excellent', 'grateful', 'blessed']
    if any(word in text_lower for word in happy_words):
        return 8
    
    very_happy_words = ['ecstatic', 'thrilled', 'overjoyed', 'elated', 'euphoric', 'blissful', 'radiant', 'incredible']
    if any(word in text_lower for word in very_happy_words):
        return 9
    
    return 5  # Default neutral

def render_quick_remedies_interface(emotion_level: int, language: str):
    """Render the comprehensive quick remedies interface."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #9D4EDD; font-size: 2.5rem;">🚀 Quick Remedies</h1>
        <p style="color: #CCCCCC; font-size: 1.1rem;">Instant relief techniques, personalized for your current mood</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced emotion-based remedy selection
    if emotion_level == 1:
        emotion_category = "Crisis/Trauma"
        color = "#8B0000"
        emoji = "💔"
        techniques = [
            {"name": "STOP Technique", "time": "1 min", "desc": "Stop, Take a breath, Observe surroundings, Proceed mindfully."},
            {"name": "Trauma Grounding", "time": "5 min", "desc": "Feel your feet on ground, name current location, date, and time."},
            {"name": "Safe Place Visualization", "time": "3 min", "desc": "Imagine a completely safe, peaceful place in vivid detail."},
            {"name": "Emergency Self-Soothing", "time": "2 min", "desc": "Hold something soft, listen to calming sounds, or smell something pleasant."}
        ]
        books = ["The Body Keeps the Score by Bessel van der Kolk", "Trauma Stewardship by Laura van Dernoot Lipsky", "Man's Search for Meaning by Viktor Frankl"]
        songs = ["Weightless by Marconi Union", "Aqueous Transmission by Incubus", "Mad World by Gary Jules"]
        jokes = [
            "What do you call a sleeping bull? A bulldozer! (Sometimes we all need rest)",
            "Why don't scientists trust atoms? They make up everything, but you're real and you matter.",
            "I told my plant a joke about gardening... but it didn't grow on them. Growth takes time."
        ]
    elif emotion_level == 2:
        emotion_category = "Very Low/Angry"
        color = "#FF4444"
        emoji = "😠"
        techniques = [
            {"name": "Anger Release Breathing", "time": "3 min", "desc": "Breathe in slowly for 4, hold for 2, exhale forcefully for 6."},
            {"name": "Progressive Muscle Tension Release", "time": "5 min", "desc": "Tense fists for 5 seconds, then release. Feel the contrast."},
            {"name": "Emotional Labeling", "time": "2 min", "desc": "Say 'I notice I'm feeling angry/sad' to create emotional distance."},
            {"name": "5-4-3-2-1 Grounding", "time": "3 min", "desc": "Name 5 things you see, 4 hear, 3 touch, 2 smell, 1 taste."}
        ]
        books = ["The Gifts of Imperfection by Brené Brown", "Anger: Wisdom for Cooling the Flames by Thich Nhat Hanh", "Permission to Feel by Marc Brackett"]
        songs = ["Breathe Me by Sia", "Heavy by Linkin Park", "Mad World by Gary Jules"]
        jokes = [
            "Why don't eggs tell jokes? They'd crack each other up! (It's okay to crack sometimes)",
            "What did the angry coffee say? I'm steamed! (Let it out safely)",
            "Why was the math book sad? Too many problems! (But every problem has a solution)"
        ]
    elif emotion_level <= 4:
        emotion_category = "Low"  
        color = "#FFA500"
        emoji = "😕"
        techniques = [
            {"name": "Box Breathing", "time": "5 min", "desc": "Breathe in 4, hold 4, out 4, hold 4. Find your rhythm."},
            {"name": "Progressive Muscle Release", "time": "10 min", "desc": "Tense and release each muscle group from toes to head."},
            {"name": "Mindful Walking", "time": "10 min", "desc": "Walk slowly, focusing on each step and your surroundings."},
            {"name": "Gratitude Reset", "time": "5 min", "desc": "Write down 3 things you're grateful for right now."}
        ]
        books = ["The Happiness Project by Gretchen Rubin", "Atomic Habits by James Clear", "Big Magic by Elizabeth Gilbert"]
        songs = ["Here Comes the Sun by The Beatles", "Good as Hell by Lizzo", "Happy by Pharrell Williams"]
        jokes = [
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the coffee file a police report? It got mugged!"
        ]
    elif emotion_level == 5:
        emotion_category = "Neutral"
        color = "#FFA500"
        emoji = "😐"
        techniques = [
            {"name": "Curiosity Activation", "time": "3 min", "desc": "Ask yourself 'What's one thing I'm curious about right now?'"},
            {"name": "Gentle Movement", "time": "5 min", "desc": "Stand up, stretch, or take a few steps to shift energy."},
            {"name": "Micro-Adventure", "time": "10 min", "desc": "Try something slightly different - new music, route, or snack."},
            {"name": "Present Moment Check-in", "time": "2 min", "desc": "Notice 3 things around you that you usually ignore."}
        ]
        books = ["The Power of Small by Linda Kaplan Thaler", "Atomic Habits by James Clear", "The Happiness Advantage by Shawn Achor"]
        songs = ["Good as Hell by Lizzo", "Sunflower by Post Malone", "Counting Stars by OneRepublic"]
        jokes = [
            "Why did the coffee file a police report? It got mugged! (Sometimes we all need a pick-me-up)",
            "What do you call a fake noodle? An impasta! (Being real is better than being fake)",
            "Why don't scientists trust stairs? They're always up to something! (Like finding new perspectives)"
        ]
    elif emotion_level == 6:
        emotion_category = "Slightly Positive"
        color = "#FFEA00"  
        emoji = "🙂"
        techniques = [
            {"name": "Energy Boost Breathing", "time": "3 min", "desc": "Quick energizing breaths to lift your spirits further."},
            {"name": "Gratitude Moment", "time": "2 min", "desc": "Name 3 small things that went well today."},
            {"name": "Positive Visualization", "time": "5 min", "desc": "Visualize yourself succeeding at something important."},
            {"name": "Connection Reach-out", "time": "5 min", "desc": "Send a positive message to someone you care about."}
        ]
        books = ["The 7 Habits of Highly Effective People by Stephen Covey", "Mindset by Carol Dweck", "The Alchemist by Paulo Coelho"]
        songs = ["Can't Stop the Feeling by Justin Timberlake", "Walking on Sunshine by Katrina and the Waves", "Don't Stop Me Now by Queen"]
        jokes = [
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't scientists trust stairs? Because they're always up to something!"
        ]
    else:
        emotion_category = "Good"
        color = "#39FF14"
        emoji = "😊"  
        techniques = [
            {"name": "Celebration Breathing", "time": "2 min", "desc": "Deep, joyful breaths to amplify your positive energy."},
            {"name": "Gratitude Expansion", "time": "5 min", "desc": "List 10 things you're grateful for and really feel each one."},
            {"name": "Energy Sharing", "time": "5 min", "desc": "Send a positive message to someone you care about."},
            {"name": "Future Visioning", "time": "5 min", "desc": "Imagine exciting possibilities for your future."}
        ]
        books = ["The Power of Positive Thinking by Norman Vincent Peale", "You Are a Badass by Jen Sincero", "The Magic by Rhonda Byrne"]
        songs = ["Good Vibrations by The Beach Boys", "I Feel Good by James Brown", "Celebration by Kool & The Gang"]
        jokes = [
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a dinosaur that crashes his car? Tyrannosaurus Wrecks!",
            "Why don't programmers like nature? It has too many bugs!"
        ]
    
    # Main remedies display
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(157, 78, 221, 0.1), rgba(58, 134, 255, 0.1)); 
         border: 2px solid {color}; border-radius: 15px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{emoji}</div>
        <h2 style="color: {color}; margin-bottom: 0.5rem;">Mood Level: {emotion_level}/10 - {emotion_category}</h2>
        <p style="color: #CCCCCC;">Personalized remedies for your current emotional state</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Techniques section
    st.markdown(f"""
    <h3 style="color: {color}; margin: 2rem 0 1rem 0;">🛠️ Instant Relief Techniques</h3>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, technique in enumerate(techniques):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background: rgba(26, 26, 26, 0.8); border: 1px solid {color}; 
                 border-radius: 10px; padding: 1rem; margin: 0.5rem 0; height: 140px;">
                <h4 style="color: {color}; margin-bottom: 0.5rem;">{technique['name']}</h4>
                <p style="color: #CCCCCC; font-size: 0.9rem; margin-bottom: 0.5rem;">{technique['desc']}</p>
                <span style="background: {color}; color: black; padding: 0.2rem 0.5rem; 
                      border-radius: 15px; font-size: 0.8rem; font-weight: bold;">⏱️ {technique['time']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Books section
    st.markdown(f"""
    <h3 style="color: {color}; margin: 2rem 0 1rem 0;">📚 Recommended Reading</h3>
    """, unsafe_allow_html=True)
    
    selected_book = random.choice(books)
    st.markdown(f"""
    <div style="background: rgba(26, 26, 26, 0.8); border: 1px solid {color}; 
         border-radius: 10px; padding: 1rem; margin: 1rem 0;">
        <h4 style="color: {color};">📖 Today's Book Suggestion</h4>
        <p style="color: #FFFFFF; font-size: 1.1rem; margin: 0.5rem 0;"><strong>{selected_book}</strong></p>
        <p style="color: #CCCCCC; font-size: 0.9rem;">Perfect for your current mood level. Reading can provide new perspectives and emotional relief.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Music section  
    st.markdown(f"""
    <h3 style="color: {color}; margin: 2rem 0 1rem 0;">🎵 Healing Music</h3>
    """, unsafe_allow_html=True)
    
    selected_song = random.choice(songs)
    st.markdown(f"""
    <div style="background: rgba(26, 26, 26, 0.8); border: 1px solid {color}; 
         border-radius: 10px; padding: 1rem; margin: 1rem 0;">
        <h4 style="color: {color};">🎶 Mood-Matching Song</h4>
        <p style="color: #FFFFFF; font-size: 1.1rem; margin: 0.5rem 0;"><strong>{selected_song}</strong></p>
        <p style="color: #CCCCCC; font-size: 0.9rem;">Music has incredible healing power. Put this on and let it work its magic!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Jokes section
    st.markdown(f"""
    <h3 style="color: {color}; margin: 2rem 0 1rem 0;">😄 Instant Smile</h3>
    """, unsafe_allow_html=True)
    
    selected_joke = random.choice(jokes)
    st.markdown(f"""
    <div style="background: rgba(26, 26, 26, 0.8); border: 1px solid {color}; 
         border-radius: 10px; padding: 1rem; margin: 1rem 0; text-align: center;">
        <h4 style="color: {color};">😂 Quick Laugh</h4>
        <p style="color: #FFFFFF; font-size: 1.1rem; margin: 1rem 0; line-height: 1.5;">{selected_joke}</p>
        <p style="color: #CCCCCC; font-size: 0.9rem;">Laughter truly is the best medicine! 🌟</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🔄 Get New Suggestions", key="refresh_remedies"):
            st.rerun()
    with col2:
        if st.button("💬 Back to Chatbot", key="remedies_to_chat"):
            st.session_state.active_view = 'chat'
            st.rerun()  
    with col3:
        if st.button("🧘‍♀️ Try Breathing", key="go_to_breathing"):
            st.session_state.active_view = 'breathing'
            st.rerun()
    with col4:
        if st.button("📷 Camera Analysis", key="go_to_camera"):
            st.session_state.active_view = 'camera'
            st.rerun()

def main():
    # Page configuration
    st.set_page_config(
        page_title="LumosAI - Mental Health Companion",
        page_icon="✨",
        layout="wide"
    )
    
    # Custom CSS for neon theme
    st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0A0A0A 0%, #1A0033 50%, #000814 100%);
        color: #FFFFFF;
    }
    
    /* Neon glow effects */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #9D4EDD, #3A86FF, #06FFA5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(157, 78, 221, 0.5);
        margin-bottom: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1A1A1A 0%, #2D1B69 100%);
        border-right: 2px solid #9D4EDD;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(26, 26, 26, 0.8);
        border-radius: 15px;
        padding: 5px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #FFFFFF;
        border-radius: 10px;
        margin: 2px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(45deg, #9D4EDD, #3A86FF);
        box-shadow: 0 0 20px rgba(157, 78, 221, 0.6);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #9D4EDD, #3A86FF);
        color: white;
        border: none;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(157, 78, 221, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(157, 78, 221, 0.8);
        transform: translateY(-2px);
    }
    
    /* Chat message styling */
    .stChatMessage {
        background: rgba(26, 26, 26, 0.6);
        border: 1px solid rgba(157, 78, 221, 0.3);
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(157, 78, 221, 0.1), rgba(58, 134, 255, 0.1));
        border: 1px solid rgba(157, 78, 221, 0.3);
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(45deg, #9D4EDD, #3A86FF);
    }
    
    /* Success/Info messages */
    .stSuccess {
        background: linear-gradient(45deg, rgba(6, 255, 165, 0.1), rgba(58, 134, 255, 0.1));
        border: 1px solid #06FFA5;
        color: #06FFA5;
    }
    
    .stInfo {
        background: linear-gradient(45deg, rgba(58, 134, 255, 0.1), rgba(157, 78, 221, 0.1));
        border: 1px solid #3A86FF;
        color: #3A86FF;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(45deg, rgba(157, 78, 221, 0.1), rgba(58, 134, 255, 0.1));
        border: 1px solid rgba(157, 78, 221, 0.3);
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Language selector (moved to sidebar in the main interface)
    selected_lang = st.session_state.language

    # Header with title and action buttons
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 1rem;">
            <h1 style="color: #9D4EDD; font-size: 2rem; margin-bottom: 0;">✨ LumosAI Therapy Companion</h1>
            <p style="color: #CCCCCC; font-size: 1rem; margin-top: 0;">A safe space for conversation and support</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Action buttons row
        col2_1, col2_2, col2_3, col2_4, col2_5, col2_6 = st.columns(6)
        
        with col2_1:
            meditation_btn = st.button("🧘‍♀️ Meditate", key="meditation_btn")
        with col2_2:
            camera_btn = st.button("📹 Camera", key="camera_btn") 
        with col2_3:
            breathe_btn = st.button("🫁 Breathe", key="breathe_btn")
        with col2_4:
            remedies_btn = st.button("🚀 Remedies", key="remedies_btn")
        with col2_5:
            challenges_btn = st.button("🎯 Challenges", key="challenges_btn")
        with col2_6:
            new_session_btn = st.button("🔄 New Session", key="new_session_btn")
    
    # Initialize session state for sidebar and sessions
    if 'sidebar_expanded' not in st.session_state:
        st.session_state.sidebar_expanded = False
    
    # Initialize sessions storage
    if 'all_sessions' not in st.session_state:
        st.session_state.all_sessions = []
    
    if 'current_session_id' not in st.session_state:
        st.session_state.current_session_id = None
    
    # Initialize session state for active view
    if 'active_view' not in st.session_state:
        st.session_state.active_view = 'chat'
    
    # Handle button clicks
    if meditation_btn:
        st.session_state.active_view = 'meditation'
    elif camera_btn:
        st.session_state.active_view = 'camera'
    elif breathe_btn:
        st.session_state.active_view = 'breathing'
    elif remedies_btn:
        st.session_state.active_view = 'remedies'
    elif challenges_btn:
        st.session_state.active_view = 'challenges'
    elif new_session_btn:
        # Save current session if it has messages
        if st.session_state.chat_history:
            session_data = {
                'id': st.session_state.current_session_id or str(datetime.now().timestamp()),
                'messages': st.session_state.chat_history.copy(),
                'emotions': st.session_state.emotion_history.copy(),
                'created_at': datetime.now().isoformat(),
                'message_count': len([m for m in st.session_state.chat_history if m.get('role') == 'user'])
            }
            st.session_state.all_sessions.append(session_data)
        
        # Start new session
        st.session_state.chat_history = []
        st.session_state.emotion_history = []
        st.session_state.current_emotion = 5
        st.session_state.last_chat_emotion = None
        st.session_state.current_session_id = str(datetime.now().timestamp())
        if hasattr(st.session_state, 'show_auto_remedies'):
            st.session_state.show_auto_remedies = False
        st.session_state.active_view = 'chat'
        st.rerun()
    
    # Layout with collapsible left sidebar
    if st.session_state.sidebar_expanded:
        left_sidebar, main_content, right_sidebar = st.columns([1, 1.5, 1])
    else:
        sidebar_toggle, main_content, right_sidebar = st.columns([0.1, 2.4, 1])
        
        # Sidebar toggle button
        with sidebar_toggle:
            st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
            if st.button("▶️", key="show_history_btn", help="Show History"):
                st.session_state.sidebar_expanded = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Left History Sidebar (when expanded)
    if st.session_state.sidebar_expanded:
        with left_sidebar:
            # Sidebar header with close button
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("### 📜 Session History")
            with col2:
                if st.button("◀️", key="hide_history_btn", help="Hide History"):
                    st.session_state.sidebar_expanded = False
                    st.rerun()
            
            # Current session
            if st.session_state.chat_history:
                st.markdown("### 💬 Current Session")
                st.markdown(f"**{len([m for m in st.session_state.chat_history if m.get('role') == 'user'])} messages**")
                
                # Show recent messages from current session
                for i, message in enumerate(st.session_state.chat_history[-3:]):  # Show last 3
                    if message["role"] == "user":
                        st.markdown(f"👤 {message['content'][:40]}...")
                    else:
                        st.markdown(f"🤖 {message['content'][:40]}...")
                
                st.markdown("---")
            
            # Previous sessions
            if st.session_state.all_sessions:
                st.markdown("### 📚 Previous Sessions")
                
                for i, session in enumerate(reversed(st.session_state.all_sessions)):
                    session_date = datetime.fromisoformat(session['created_at']).strftime('%m/%d %H:%M')
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        if st.button(f"Session {len(st.session_state.all_sessions) - i}: {session['message_count']} messages", 
                                   key=f"load_session_{session['id']}", help=f"Created: {session_date}"):
                            # Save current session first if it has content
                            if st.session_state.chat_history:
                                current_session = {
                                    'id': st.session_state.current_session_id or str(datetime.now().timestamp()),
                                    'messages': st.session_state.chat_history.copy(),
                                    'emotions': st.session_state.emotion_history.copy(),
                                    'created_at': datetime.now().isoformat(),
                                    'message_count': len([m for m in st.session_state.chat_history if m.get('role') == 'user'])
                                }
                                # Remove if already exists, then add updated version
                                st.session_state.all_sessions = [s for s in st.session_state.all_sessions if s['id'] != current_session['id']]
                                st.session_state.all_sessions.append(current_session)
                            
                            # Load selected session
                            st.session_state.chat_history = session['messages'].copy()
                            st.session_state.emotion_history = session['emotions'].copy()
                            st.session_state.current_session_id = session['id']
                            st.rerun()
                    
                    with col2:
                        st.caption(session_date)
                    
                    with col3:
                        if st.button("🗑️", key=f"delete_session_{session['id']}", help="Delete session"):
                            st.session_state.all_sessions = [s for s in st.session_state.all_sessions if s['id'] != session['id']]
                            
                            # If we just deleted the last session and current session is empty, start fresh
                            if not st.session_state.all_sessions and not st.session_state.chat_history:
                                st.session_state.current_session_id = str(datetime.now().timestamp())
                                st.session_state.current_emotion = 5
                                st.session_state.last_chat_emotion = None
                                if hasattr(st.session_state, 'show_auto_remedies'):
                                    st.session_state.show_auto_remedies = False
                            
                            st.rerun()
            else:
                if not st.session_state.chat_history:
                    st.info("No sessions yet. Start chatting to create your first session!")
            
            # Add "Delete All Sessions" button if there are any sessions
            if st.session_state.all_sessions:
                st.markdown("---")
                if st.button("🗑️ Delete All Sessions", key="delete_all_sessions", type="secondary"):
                    st.session_state.all_sessions = []
                    
                    # If current session is also empty, start a fresh session
                    if not st.session_state.chat_history:
                        st.session_state.current_session_id = str(datetime.now().timestamp())
                        st.session_state.current_emotion = 5
                        st.session_state.last_chat_emotion = None
                        if hasattr(st.session_state, 'show_auto_remedies'):
                            st.session_state.show_auto_remedies = False
                    
                    st.success("All sessions deleted!")
                    st.rerun()
    
    # Main content area
    with main_content:
        if st.session_state.active_view == 'chat':
            # Chat interface
            if not st.session_state.chat_history:
                # Initial AI message
                st.markdown("""
                <div style="background: rgba(157, 78, 221, 0.1); border: 1px solid rgba(157, 78, 221, 0.3); border-radius: 15px; padding: 1rem; margin-bottom: 1rem;">
                    <div style="color: #9D4EDD; font-weight: bold; margin-bottom: 0.5rem;">🤖 AI Therapist</div>
                    <div style="color: #FFFFFF;">Hello, I'm your AI therapy companion. I'm here to listen and provide support in a safe, judgment-free environment. How are you feeling today?</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Display chat history
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div style="background: rgba(58, 134, 255, 0.1); border: 1px solid rgba(58, 134, 255, 0.3); border-radius: 15px; padding: 1rem; margin: 1rem 0; margin-left: 2rem;">
                        <div style="color: #3A86FF; font-weight: bold; margin-bottom: 0.5rem;">👤 You</div>
                        <div style="color: #FFFFFF;">{message["content"]}</div>
                        {f'<small style="color: #CCCCCC;">Emotion: {message.get("emotion", 5)}/10</small>' if "emotion" in message else ''}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(157, 78, 221, 0.1); border: 1px solid rgba(157, 78, 221, 0.3); border-radius: 15px; padding: 1rem; margin: 1rem 0; margin-right: 2rem;">
                        <div style="color: #9D4EDD; font-weight: bold; margin-bottom: 0.5rem;">🤖 AI Therapist</div>
                        <div style="color: #FFFFFF;">{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Auto-remedies notification for low emotions
            if hasattr(st.session_state, 'show_auto_remedies') and st.session_state.show_auto_remedies:
                st.markdown("""
                <div style="background: rgba(255, 107, 107, 0.1); border: 1px solid rgba(255, 107, 107, 0.3); border-radius: 15px; padding: 1rem; margin: 1rem 0;">
                    <div style="color: #FF6B6B; font-weight: bold; margin-bottom: 0.5rem;">💡 Quick Relief Suggestion</div>
                    <div style="color: #FFFFFF; margin-bottom: 1rem;">I noticed you might be feeling low. Would you like some instant relief techniques?</div>
                    <div style="display: flex; gap: 0.5rem;">
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🚀 View Remedies", key="auto_remedies_btn"):
                        st.session_state.active_view = 'remedies'
                        st.session_state.show_auto_remedies = False
                        st.rerun()
                with col2:
                    if st.button("🧘‍♀️ Quick Breathing", key="auto_breathing_btn"):
                        st.session_state.active_view = 'breathing'
                        st.session_state.show_auto_remedies = False
                        st.rerun()
                with col3:
                    if st.button("❌ Dismiss", key="dismiss_auto_btn"):
                        st.session_state.show_auto_remedies = False
                        st.rerun()
                
                st.markdown("</div></div>", unsafe_allow_html=True)
            
            # Chat input
            if prompt := st.chat_input(get_text("chat_placeholder", st.session_state.language)):
                # Detect emotion from user input
                detected_emotion = detect_emotion_from_text(prompt)
                st.session_state.last_chat_emotion = detected_emotion
                st.session_state.current_emotion = detected_emotion
                
                # Add emotion to history
                emotion_entry = {
                    "emotion": detected_emotion,
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state.emotion_history.append(emotion_entry)
                
                # Initialize session ID if not exists
                if not st.session_state.current_session_id:
                    st.session_state.current_session_id = str(datetime.now().timestamp())
                
                # Add user message
                user_message = {
                    "role": "user",
                    "content": prompt,
                    "timestamp": datetime.now().isoformat(),
                    "emotion": detected_emotion
                }
                st.session_state.chat_history.append(user_message)
                
                # Get bot response
                with st.spinner(get_text("thinking", st.session_state.language)):
                    response = st.session_state.therapy_bot.get_response(
                        prompt, 
                        st.session_state.language,
                        detected_emotion,
                        st.session_state.chat_history[-5:]  # Last 5 messages for context
                    )
                
                # Add bot message
                bot_message = {
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state.chat_history.append(bot_message)
                
                # Auto-suggest remedies for low emotions (1-4)
                if detected_emotion <= 4:
                    st.session_state.show_auto_remedies = True
                
                st.rerun()
        
        elif st.session_state.active_view == 'camera':
            st.session_state.camera_analysis.display_camera_interface(st.session_state.language)
            
        elif st.session_state.active_view == 'breathing':
            st.session_state.breathing_exercises.display_breathing_interface(st.session_state.language)
            
        elif st.session_state.active_view == 'meditation':
            st.session_state.meditation_module.display_meditation_interface(
                st.session_state.language, 
                st.session_state.current_emotion
            )
            
        elif st.session_state.active_view == 'remedies':
            render_quick_remedies_interface(st.session_state.current_emotion, st.session_state.language)
            
        elif st.session_state.active_view == 'challenges':
            st.session_state.daily_challenges.render_challenges_tab(st.session_state.language)
            

    # Right sidebar - Visual & Emotional Insights  
    with right_sidebar:
        st.markdown("""
        <div style="text-align: center; font-size: 1.3rem; color: #9D4EDD; margin-bottom: 1rem; font-weight: bold;">
            📊 Visual & Emotional Insights
        </div>
        """, unsafe_allow_html=True)
        
        # Camera Feed Section
        st.markdown("""
        <div style="background: rgba(26, 26, 26, 0.8); border: 1px solid rgba(157, 78, 221, 0.3); border-radius: 15px; padding: 1rem; margin-bottom: 1.5rem;">
            <div style="color: #FFFFFF; font-weight: bold; margin-bottom: 0.5rem;">📹 Camera Feed</div>
        """, unsafe_allow_html=True)
        
        # Camera status and controls
        if len(st.session_state.camera_analysis.emotion_data) > 0:
            latest_emotion = st.session_state.camera_analysis.emotion_data[-1]
            st.success(f"📸 Last Analysis: {latest_emotion['primary_emotion'].title()}")
            st.markdown(f"<small style='color: #CCCCCC;'>Confidence: {latest_emotion['confidence']:.1f}%</small>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(40, 40, 40, 0.5); border-radius: 10px; margin: 1rem 0;">
                <div style="color: #666; font-size: 3rem;">📸</div>
                <div style="color: #CCCCCC; margin-top: 0.5rem;">No emotion analysis yet</div>
                <div style="color: #999; font-size: 0.9rem;">Take or upload a photo to analyze emotions</div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("📷 Open Camera Analysis", key="open_camera_sidebar"):
            st.session_state.active_view = 'camera'
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # AI-Detected Emotion Display
        st.markdown("""
        <div style="background: rgba(26, 26, 26, 0.8); border: 1px solid rgba(157, 78, 221, 0.3); border-radius: 15px; padding: 1rem;">
            <div style="color: #FFFFFF; font-weight: bold; margin-bottom: 1rem;">🤖 AI Emotion Analysis</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get current detected emotion from chat or camera
        detected_emotion = get_current_detected_emotion()
        
        if detected_emotion:
            emotion_faces = {
                1: "💔", 2: "😠", 3: "😕", 4: "😐", 5: "😶",
                6: "🙂", 7: "😊", 8: "😄", 9: "😁", 10: "🤩"
            }
            
            emotion_labels = {
                1: "Crisis/Trauma", 2: "Angry/Very Sad", 3: "Down", 4: "Low", 5: "Neutral",
                6: "Okay", 7: "Good", 8: "Happy", 9: "Very Happy", 10: "Excellent"
            }
            
            st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <div style="font-size: 3rem;">{emotion_faces.get(detected_emotion, "😶")}</div>
                <div style="color: #FFFFFF; font-size: 1.2rem; margin-top: 0.5rem;">Detected: {emotion_labels.get(detected_emotion, "Neutral")}</div>
                <div style="color: #9D4EDD; font-size: 0.9rem;">Based on your conversation & camera</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Update current emotion with detected value
            st.session_state.current_emotion = detected_emotion
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: rgba(40, 40, 40, 0.5); border-radius: 10px; margin: 1rem 0;">
                <div style="color: #666; font-size: 3rem;">🤖</div>
                <div style="color: #CCCCCC; margin-top: 0.5rem;">No emotion detected yet</div>
                <div style="color: #999; font-size: 0.9rem;">Chat or take a photo to analyze emotions</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Daily Challenges Progress
        st.markdown("---")
        st.markdown("**🎯 Daily Challenge**")
        
        # Show current challenge status
        challenge_stats = st.session_state.daily_challenges.get_streak_info()
        challenge = st.session_state.daily_challenges.get_daily_challenge('beginner')
        
        if challenge and not challenge.get('completed', False):
            st.markdown(f"""
            <div style="background: rgba(157, 78, 221, 0.1); border: 1px solid rgba(157, 78, 221, 0.3); border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
                <div style="color: #9D4EDD; font-weight: bold; font-size: 0.9rem; margin-bottom: 0.5rem;">{challenge['title']}</div>
                <div style="color: #CCCCCC; font-size: 0.8rem;">{challenge['description'][:50]}...</div>
                <div style="color: #39FF14; font-size: 0.8rem; margin-top: 0.5rem;">+{challenge['points']} points</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("🎉 Today's challenge completed!")
        
        if st.button("🎯 View Challenges", key="view_challenges_sidebar"):
            st.session_state.active_view = 'challenges'
            st.rerun()
        
        # Quick stats
        st.markdown("---")
        st.markdown("**📈 Session Stats**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", len([m for m in st.session_state.chat_history if m.get('role') == 'user']))
            st.metric("🔥 Streak", f"{challenge_stats['current_streak']} days")
        with col2:
            detected_emotion = get_current_detected_emotion()
            if detected_emotion:
                avg_emotion = sum([e['emotion'] for e in st.session_state.emotion_history]) / len(st.session_state.emotion_history) if st.session_state.emotion_history else detected_emotion
                st.metric("Avg Mood", f"{avg_emotion:.1f}/10")
            else:
                st.metric("Avg Mood", "Not detected")
            st.metric("💎 Points", challenge_stats['total_points'])
        
        # Language selector
        st.markdown("---")
        st.markdown("**🌐 Language / भाषा**")
        
        selected_lang = st.selectbox(
            "Select Language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x],
            index=0 if st.session_state.language == 'en' else 1,
            key="lang_selector"
        )
        
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()
        
        
        # Export data
        st.markdown("---")
        if st.button("📥 Export Data", key="export_data_sidebar"):
            data = st.session_state.data_manager.export_all_data(
                st.session_state.chat_history,
                st.session_state.emotion_history
            )
            st.download_button(
                label="Download JSON",
                data=data,
                file_name=f"lumosai_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key="download_data"
            )

if __name__ == "__main__":
    main()
