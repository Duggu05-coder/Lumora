import streamlit as st
import time
import numpy as np
from datetime import datetime
from typing import Dict, List
from translations import get_text

class MeditationModule:
    def __init__(self):
        """Initialize meditation module with session tracking."""
        self.meditation_sessions = []
        self.current_session = None
        self.is_active = False
        
    def display_meditation_interface(self, language: str, current_emotion: int):
        """
        Display meditation and mindfulness interface.
        
        Args:
            language: Current language ('en' or 'hi')
            current_emotion: Current emotion level (1-10)
        """
        st.header("🧘‍♀️ Meditation & Mindfulness")
        
        # Welcome section
        st.markdown("""
        <div style="background: rgba(157, 78, 221, 0.1); border: 1px solid rgba(157, 78, 221, 0.3); border-radius: 15px; padding: 1.5rem; margin: 1rem 0;">
            <div style="color: #9D4EDD; font-weight: bold; margin-bottom: 1rem;">🌸 Welcome to Your Mindfulness Space</div>
            <div style="color: #FFFFFF;">
                Find inner peace and emotional balance through guided meditation and mindfulness practices. 
                Each session is personalized based on your current emotional state.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Meditation type selection based on emotion
        st.subheader("🎯 Recommended Practice")
        recommended_meditation = self._get_emotion_based_meditation(current_emotion, language)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background: rgba(58, 134, 255, 0.1); border: 1px solid rgba(58, 134, 255, 0.3); border-radius: 10px; padding: 1rem;">
                <div style="color: #3A86FF; font-weight: bold;">{recommended_meditation['name']}</div>
                <div style="color: #CCCCCC; margin-top: 0.5rem;">{recommended_meditation['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            if st.button("🎧 Start Recommended", type="primary", key="start_recommended"):
                self._start_meditation_session(recommended_meditation, current_emotion, language)
        
        st.divider()
        
        # All meditation types
        st.subheader("🌟 All Meditation Types")
        meditation_types = self._get_all_meditations(language)
        
        for meditation in meditation_types:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="padding: 0.5rem;">
                    <div style="color: #FFFFFF; font-weight: bold;">{meditation['icon']} {meditation['name']}</div>
                    <div style="color: #CCCCCC; font-size: 0.9rem;">{meditation['description']}</div>
                    <div style="color: #9D4EDD; font-size: 0.8rem;">Duration: {meditation['duration']} min</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🎧 Start", key=f"start_{meditation['id']}"):
                    self._start_meditation_session(meditation, current_emotion, language)
            
            with col3:
                st.markdown(f"<div style='text-align: center; color: #39FF14;'>{meditation['difficulty']}</div>", unsafe_allow_html=True)
        
        # Active session display
        if self.is_active and self.current_session:
            self._display_active_session(language)
        
        # Session history
        if self.meditation_sessions:
            self._display_session_history(language)
        
        # Back to Chatbot button
        st.markdown("---")
        if st.button("💬 Back to Chatbot", key="meditation_to_chat", type="secondary"):
            st.session_state.active_view = 'chat'
            st.rerun()
    
    def _get_emotion_based_meditation(self, emotion_level: int, language: str) -> Dict:
        """Get recommended meditation based on emotion level."""
        meditations = {
            'en': {
                'low': {
                    'name': 'Compassion & Self-Love Meditation',
                    'description': 'Gentle practice to nurture self-compassion and emotional healing',
                    'type': 'compassion',
                    'duration': 10,
                    'icon': '💝'
                },
                'medium': {
                    'name': 'Mindful Awareness Meditation',
                    'description': 'Build present-moment awareness and emotional stability',
                    'type': 'mindfulness',
                    'duration': 15,
                    'icon': '🌺'
                },
                'high': {
                    'name': 'Gratitude & Joy Meditation',
                    'description': 'Amplify positive emotions and cultivate gratitude',
                    'type': 'gratitude',
                    'duration': 12,
                    'icon': '✨'
                }
            },
            'hi': {
                'low': {
                    'name': 'करुणा और स्व-प्रेम ध्यान',
                    'description': 'स्व-करुणा और भावनात्मक चिकित्सा के लिए कोमल अभ्यास',
                    'type': 'compassion',
                    'duration': 10,
                    'icon': '💝'
                },
                'medium': {
                    'name': 'सचेत जागरूकता ध्यान',
                    'description': 'वर्तमान क्षण की जागरूकता और भावनात्मक स्थिरता बनाएं',
                    'type': 'mindfulness',
                    'duration': 15,
                    'icon': '🌺'
                },
                'high': {
                    'name': 'कृतज्ञता और आनंद ध्यान',
                    'description': 'सकारात्मक भावनाओं को बढ़ाएं और कृतज्ञता विकसित करें',
                    'type': 'gratitude',
                    'duration': 12,
                    'icon': '✨'
                }
            }
        }
        
        if emotion_level <= 4:
            category = 'low'
        elif emotion_level <= 7:
            category = 'medium'
        else:
            category = 'high'
            
        return meditations[language][category]
    
    def _get_all_meditations(self, language: str) -> List[Dict]:
        """Get all available meditation types."""
        if language == 'hi':
            return [
                {
                    'id': 'breathing',
                    'name': 'श्वास ध्यान',
                    'description': 'गहरी सांस लेने पर ध्यान केंद्रित करें',
                    'duration': 5,
                    'difficulty': 'आसान',
                    'icon': '🫁',
                    'type': 'breathing'
                },
                {
                    'id': 'body_scan',
                    'name': 'शरीर स्कैन ध्यान',
                    'description': 'शरीर के हर हिस्से में तनाव मुक्ति',
                    'duration': 20,
                    'difficulty': 'मध्यम',
                    'icon': '🌊',
                    'type': 'body_scan'
                },
                {
                    'id': 'loving_kindness',
                    'name': 'मैत्री ध्यान',
                    'description': 'प्रेम और दया की भावनाओं को विकसित करें',
                    'duration': 15,
                    'difficulty': 'मध्यम',
                    'icon': '💖',
                    'type': 'loving_kindness'
                },
                {
                    'id': 'walking',
                    'name': 'चलते हुए ध्यान',
                    'description': 'चलते समय सचेत रहने का अभ्यास',
                    'duration': 10,
                    'difficulty': 'आसान',
                    'icon': '🚶‍♀️',
                    'type': 'walking'
                },
                {
                    'id': 'visualization',
                    'name': 'दृश्यीकरण ध्यान',
                    'description': 'शांत दृश्यों की कल्पना करें',
                    'duration': 12,
                    'difficulty': 'मध्यम',
                    'icon': '🏔️',
                    'type': 'visualization'
                }
            ]
        else:
            return [
                {
                    'id': 'breathing',
                    'name': 'Breathing Meditation',
                    'description': 'Focus on deep, mindful breathing patterns',
                    'duration': 5,
                    'difficulty': 'Easy',
                    'icon': '🫁',
                    'type': 'breathing'
                },
                {
                    'id': 'body_scan',
                    'name': 'Body Scan Meditation',
                    'description': 'Progressive relaxation through body awareness',
                    'duration': 20,
                    'difficulty': 'Medium',
                    'icon': '🌊',
                    'type': 'body_scan'
                },
                {
                    'id': 'loving_kindness',
                    'name': 'Loving-Kindness Meditation',
                    'description': 'Cultivate compassion and loving feelings',
                    'duration': 15,
                    'difficulty': 'Medium',
                    'icon': '💖',
                    'type': 'loving_kindness'
                },
                {
                    'id': 'walking',
                    'name': 'Walking Meditation',
                    'description': 'Mindful awareness while walking',
                    'duration': 10,
                    'difficulty': 'Easy',
                    'icon': '🚶‍♀️',
                    'type': 'walking'
                },
                {
                    'id': 'visualization',
                    'name': 'Visualization Meditation',
                    'description': 'Guided imagery for peace and relaxation',
                    'duration': 12,
                    'difficulty': 'Medium',
                    'icon': '🏔️',
                    'type': 'visualization'
                }
            ]
    
    def _start_meditation_session(self, meditation: Dict, initial_emotion: int, language: str):
        """Start a meditation session with emotion tracking."""
        self.is_active = True
        self.current_session = {
            'meditation': meditation,
            'start_time': datetime.now(),
            'initial_emotion': initial_emotion,
            'language': language,
            'progress': 0,
            'emotion_tracking': [{'time': 0, 'emotion': initial_emotion}]
        }
        st.success(f"🧘‍♀️ Starting {meditation['name']} session...")
        st.rerun()
    
    def _display_active_session(self, language: str):
        """Display active meditation session interface."""
        st.markdown("---")
        st.subheader("🎧 Active Meditation Session")
        
        session = self.current_session
        meditation = session['meditation']
        
        # Session info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Session Type", meditation['name'])
        
        with col2:
            elapsed_time = (datetime.now() - session['start_time']).total_seconds() / 60
            st.metric("Time Elapsed", f"{elapsed_time:.1f} min")
        
        with col3:
            progress = min(100, (elapsed_time / meditation['duration']) * 100)
            st.metric("Progress", f"{progress:.0f}%")
        
        # Progress bar
        st.progress(progress / 100)
        
        # Meditation guidance based on type
        guidance = self._get_meditation_guidance(meditation['type'], language, elapsed_time)
        st.markdown(f"""
        <div style="background: rgba(157, 78, 221, 0.1); border: 1px solid rgba(157, 78, 221, 0.3); border-radius: 15px; padding: 1.5rem; margin: 1rem 0;">
            <div style="color: #9D4EDD; font-weight: bold; margin-bottom: 1rem;">🧘‍♀️ Current Guidance</div>
            <div style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.6;">
                {guidance}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Real-time emotion tracking
        st.subheader("💜 How are you feeling right now?")
        current_emotion = st.slider(
            "Rate your current emotional state",
            min_value=1,
            max_value=10,
            value=session['initial_emotion'],
            key=f"meditation_emotion_{len(session['emotion_tracking'])}"
        )
        
        # Update emotion tracking
        if current_emotion != session['emotion_tracking'][-1]['emotion']:
            session['emotion_tracking'].append({
                'time': elapsed_time,
                'emotion': current_emotion
            })
        
        # Session controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⏸️ Pause", key="pause_meditation"):
                st.info("Session paused. Take your time.")
        
        with col2:
            if st.button("⏭️ Next Phase", key="next_phase"):
                session['progress'] += 25
                st.success("Moving to next phase...")
        
        with col3:
            if st.button("✅ Complete Session", key="complete_meditation"):
                self._complete_meditation_session()
                st.success("🎉 Meditation session completed!")
                st.rerun()
    
    def _get_meditation_guidance(self, meditation_type: str, language: str, elapsed_time: float) -> str:
        """Get meditation guidance based on type and elapsed time."""
        guidance_texts = {
            'breathing': {
                'en': [
                    "Begin by finding a comfortable position. Close your eyes and take three deep breaths.",
                    "Focus on your natural breath. Feel the air entering and leaving your nostrils.",
                    "If your mind wanders, gently bring your attention back to your breath.",
                    "Notice the pause between each inhale and exhale. Rest in this peaceful space."
                ],
                'hi': [
                    "आरामदायक स्थिति में बैठें। अपनी आंखें बंद करें और तीन गहरी सांसें लें।",
                    "अपनी प्राकृतिक सांस पर ध्यान दें। हवा को नासिका में आते-जाते महसूस करें।",
                    "यदि मन भटके, तो धीरे से अपना ध्यान सांस पर वापस लाएं।",
                    "प्रत्येक सांस के बीच के विराम को महसूस करें। इस शांत स्थान में विश्राम करें।"
                ]
            },
            'body_scan': {
                'en': [
                    "Lie down comfortably and close your eyes. Start by noticing your toes.",
                    "Slowly move your attention up through your legs, feeling each part relax.",
                    "Continue scanning through your torso, arms, and shoulders, releasing tension.",
                    "Finally, relax your neck, face, and head. Feel your whole body at peace."
                ],
                'hi': [
                    "आराम से लेटें और आंखें बंद करें। अपने पैर की उंगलियों को महसूस करें।",
                    "धीरे-धीरे अपना ध्यान पैरों से ऊपर ले जाएं, हर हिस्से को आराम देते हुए।",
                    "धड़, बाहों और कंधों को स्कैन करते हुए तनाव को मुक्त करें।",
                    "अंत में गर्दन, चेहरे और सिर को आराम दें। पूरे शरीर को शांति में महसूस करें।"
                ]
            },
            'loving_kindness': {
                'en': [
                    "Place your hand on your heart. Send loving-kindness to yourself: 'May I be happy.'",
                    "Extend this love to someone you care about: 'May you be peaceful and free from suffering.'",
                    "Now include someone neutral: 'May you find happiness and inner peace.'",
                    "Finally, send love to all beings everywhere: 'May all beings be happy and free.'"
                ],
                'hi': [
                    "अपना हाथ हृदय पर रखें। स्वयं को प्रेम भेजें: 'मैं खुश रहूं।'",
                    "इस प्रेम को किसी प्रिय व्यक्ति तक फैलाएं: 'आप शांत और दुख से मुक्त रहें।'",
                    "अब किसी तटस्थ व्यक्ति को शामिल करें: 'आपको खुशी और शांति मिले।'",
                    "अंत में सभी प्राणियों को प्रेम भेजें: 'सभी प्राणी खुश और मुक्त रहें।'"
                ]
            }
        }
        
        # Get appropriate guidance phase based on elapsed time
        guidance_list = guidance_texts.get(meditation_type, guidance_texts['breathing'])[language]
        phase = min(int(elapsed_time / 2), len(guidance_list) - 1)  # Change guidance every 2 minutes
        
        return guidance_list[phase]
    
    def _complete_meditation_session(self):
        """Complete the current meditation session and save data."""
        if not self.current_session:
            return
        
        session = self.current_session.copy()
        session['end_time'] = datetime.now()
        session['duration'] = (session['end_time'] - session['start_time']).total_seconds() / 60
        session['final_emotion'] = session['emotion_tracking'][-1]['emotion']
        session['emotion_change'] = session['final_emotion'] - session['initial_emotion']
        
        # Calculate session metrics
        session['effectiveness'] = self._calculate_effectiveness(session)
        
        self.meditation_sessions.append(session)
        self.is_active = False
        self.current_session = None
    
    def _calculate_effectiveness(self, session: Dict) -> float:
        """Calculate meditation session effectiveness based on emotion changes."""
        emotion_changes = [
            track['emotion'] for track in session['emotion_tracking']
        ]
        
        if len(emotion_changes) < 2:
            return 0.0
        
        # Calculate improvement trend
        initial = emotion_changes[0]
        final = emotion_changes[-1]
        improvement = final - initial
        
        # Normalize to 0-1 scale
        effectiveness = max(0, min(1, (improvement + 5) / 10))
        
        return effectiveness
    
    def _display_session_history(self, language: str):
        """Display meditation session history and analytics."""
        st.markdown("---")
        st.subheader("📊 Meditation History & Progress")
        
        # Recent sessions
        recent_sessions = self.meditation_sessions[-5:]  # Last 5 sessions
        
        for session in reversed(recent_sessions):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"**{session['meditation']['icon']} {session['meditation']['name']}**")
                st.caption(f"{session['start_time'].strftime('%Y-%m-%d %H:%M')}")
            
            with col2:
                st.metric("Duration", f"{session['duration']:.1f} min")
            
            with col3:
                emotion_change = session['emotion_change']
                delta_color = "normal" if emotion_change >= 0 else "inverse"
                st.metric("Emotion Change", f"{emotion_change:+.1f}", delta=f"{emotion_change:+.1f}")
            
            with col4:
                effectiveness = session['effectiveness'] * 100
                st.metric("Effectiveness", f"{effectiveness:.0f}%")
        
        # Overall statistics
        if len(self.meditation_sessions) >= 3:
            st.subheader("🌟 Your Meditation Journey")
            
            total_sessions = len(self.meditation_sessions)
            total_time = sum(session['duration'] for session in self.meditation_sessions)
            avg_improvement = sum(session['emotion_change'] for session in self.meditation_sessions) / total_sessions
            avg_effectiveness = sum(session['effectiveness'] for session in self.meditation_sessions) / total_sessions
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Sessions", total_sessions)
            
            with col2:
                st.metric("Total Time", f"{total_time:.1f} min")
            
            with col3:
                st.metric("Avg Improvement", f"{avg_improvement:+.1f}")
            
            with col4:
                st.metric("Avg Effectiveness", f"{avg_effectiveness * 100:.0f}%")
    
    def get_session_data(self) -> List[Dict]:
        """Get all meditation session data for export."""
        return self.meditation_sessions
    
    def clear_session_data(self):
        """Clear all meditation session data."""
        self.meditation_sessions = []
        self.current_session = None
        self.is_active = False