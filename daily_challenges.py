import streamlit as st
import random
from datetime import datetime, timedelta
import json
from typing import Dict, List

class DailyChallenges:
    def __init__(self):
        if 'daily_challenges_data' not in st.session_state:
            st.session_state.daily_challenges_data = {
                'current_challenge': None,
                'completed_challenges': [],
                'challenge_history': [],
                'streak': 0,
                'last_completed': None,
                'total_points': 0
            }
        
        self.challenges_data = self._load_challenges()
    
    def _load_challenges(self) -> Dict:
        """Load daily challenges data."""
        return {
            'beginner': {
                'mindfulness': [
                    {
                        'title': 'Mindful Morning',
                        'description': 'Spend 5 minutes focusing on your breath when you wake up',
                        'instructions': 'Sit quietly, close your eyes, and breathe naturally. Count each breath from 1 to 10, then start over.',
                        'duration': '5 minutes',
                        'points': 10,
                        'category': 'Mindfulness'
                    },
                    {
                        'title': 'Gratitude Practice',
                        'description': 'Write down 3 things you are grateful for today',
                        'instructions': 'Take a moment to think about what went well today. Write down 3 specific things you appreciate.',
                        'duration': '3 minutes',
                        'points': 10,
                        'category': 'Gratitude'
                    },
                    {
                        'title': 'Body Scan Check-in',
                        'description': 'Do a quick body scan to notice tension',
                        'instructions': 'Start from your toes and slowly move up to your head. Notice any areas of tension without trying to change them.',
                        'duration': '5 minutes',
                        'points': 15,
                        'category': 'Body Awareness'
                    }
                ],
                'self_care': [
                    {
                        'title': 'Hydration Hero',
                        'description': 'Drink 8 glasses of water throughout the day',
                        'instructions': 'Keep a water bottle nearby and take sips regularly. Notice how proper hydration affects your mood.',
                        'duration': 'All day',
                        'points': 15,
                        'category': 'Physical Health'
                    },
                    {
                        'title': 'Digital Detox Hour',
                        'description': 'Spend 1 hour without any digital devices',
                        'instructions': 'Put away your phone, computer, and TV. Read a book, go for a walk, or have a conversation.',
                        'duration': '1 hour',
                        'points': 20,
                        'category': 'Digital Wellness'
                    },
                    {
                        'title': 'Nature Connection',
                        'description': 'Spend 10 minutes outdoors in nature',
                        'instructions': 'Go outside and observe the natural world around you. Feel the sun, breeze, or notice plants and animals.',
                        'duration': '10 minutes',
                        'points': 15,
                        'category': 'Nature'
                    }
                ],
                'social': [
                    {
                        'title': 'Kindness Spread',
                        'description': 'Do one small act of kindness for someone',
                        'instructions': 'Send a supportive message, help a neighbor, or simply smile at strangers you meet.',
                        'duration': '5 minutes',
                        'points': 15,
                        'category': 'Kindness'
                    },
                    {
                        'title': 'Quality Connection',
                        'description': 'Have a meaningful conversation with someone you care about',
                        'instructions': 'Put away distractions and really listen. Ask open-ended questions and share authentically.',
                        'duration': '15 minutes',
                        'points': 20,
                        'category': 'Connection'
                    }
                ]
            },
            'intermediate': {
                'mindfulness': [
                    {
                        'title': 'Mindful Eating',
                        'description': 'Eat one meal completely mindfully',
                        'instructions': 'Eat slowly, notice textures, flavors, and how the food makes you feel. No distractions.',
                        'duration': '20 minutes',
                        'points': 25,
                        'category': 'Mindful Living'
                    },
                    {
                        'title': 'Walking Meditation',
                        'description': 'Take a 15-minute mindful walk',
                        'instructions': 'Walk slowly and deliberately. Focus on each step, your surroundings, and your breathing.',
                        'duration': '15 minutes',
                        'points': 20,
                        'category': 'Movement'
                    }
                ],
                'emotional': [
                    {
                        'title': 'Emotion Journaling',
                        'description': 'Write about your emotions for 10 minutes',
                        'instructions': 'Describe what you felt today, what triggered these emotions, and how you responded.',
                        'duration': '10 minutes',
                        'points': 20,
                        'category': 'Emotional Intelligence'
                    },
                    {
                        'title': 'Forgiveness Practice',
                        'description': 'Practice forgiving yourself or someone else',
                        'instructions': 'Think of a situation that bothers you. Try to understand all perspectives and let go of resentment.',
                        'duration': '10 minutes',
                        'points': 30,
                        'category': 'Forgiveness'
                    }
                ]
            },
            'advanced': {
                'mindfulness': [
                    {
                        'title': 'Silent Observation',
                        'description': 'Sit in silence for 20 minutes observing thoughts',
                        'instructions': 'Sit quietly and observe your thoughts without judgment. Notice patterns and let thoughts pass by.',
                        'duration': '20 minutes',
                        'points': 35,
                        'category': 'Deep Practice'
                    }
                ],
                'growth': [
                    {
                        'title': 'Fear Facing',
                        'description': 'Do one thing that scares you (but is safe)',
                        'instructions': 'Identify a fear that holds you back and take one small step toward facing it today.',
                        'duration': 'Varies',
                        'points': 40,
                        'category': 'Personal Growth'
                    },
                    {
                        'title': 'Value Reflection',
                        'description': 'Identify and reflect on your core values',
                        'instructions': 'Write down your top 5 values and think about how well your current life aligns with them.',
                        'duration': '15 minutes',
                        'points': 30,
                        'category': 'Self-Discovery'
                    }
                ]
            }
        }
    
    def get_daily_challenge(self, difficulty: str = 'beginner') -> Dict:
        """Get today's daily challenge."""
        today = datetime.now().date()
        
        # Check if we already have a challenge for today
        if (st.session_state.daily_challenges_data['current_challenge'] and 
            st.session_state.daily_challenges_data['current_challenge'].get('date') == str(today)):
            return st.session_state.daily_challenges_data['current_challenge']
        
        # Generate new challenge for today
        categories = list(self.challenges_data[difficulty].keys())
        selected_category = random.choice(categories)
        challenges_in_category = self.challenges_data[difficulty][selected_category]
        selected_challenge = random.choice(challenges_in_category)
        
        # Add metadata
        selected_challenge['date'] = str(today)
        selected_challenge['difficulty'] = difficulty
        selected_challenge['completed'] = False
        
        # Store in session state
        st.session_state.daily_challenges_data['current_challenge'] = selected_challenge
        
        return selected_challenge
    
    def mark_challenge_complete(self, challenge: Dict):
        """Mark current challenge as completed."""
        today = datetime.now().date()
        
        if challenge and not challenge.get('completed'):
            # Mark as completed
            challenge['completed'] = True
            challenge['completed_date'] = str(today)
            
            # Add to completed challenges
            st.session_state.daily_challenges_data['completed_challenges'].append(challenge)
            st.session_state.daily_challenges_data['challenge_history'].append(challenge)
            
            # Update streak
            last_completed = st.session_state.daily_challenges_data['last_completed']
            if last_completed:
                last_date = datetime.strptime(last_completed, '%Y-%m-%d').date()
                if today - last_date == timedelta(days=1):
                    st.session_state.daily_challenges_data['streak'] += 1
                elif today - last_date > timedelta(days=1):
                    st.session_state.daily_challenges_data['streak'] = 1
            else:
                st.session_state.daily_challenges_data['streak'] = 1
            
            # Update points and last completed date
            st.session_state.daily_challenges_data['total_points'] += challenge.get('points', 0)
            st.session_state.daily_challenges_data['last_completed'] = str(today)
            
            return True
        return False
    
    def get_streak_info(self) -> Dict:
        """Get current streak information."""
        return {
            'current_streak': st.session_state.daily_challenges_data['streak'],
            'total_points': st.session_state.daily_challenges_data['total_points'],
            'total_completed': len(st.session_state.daily_challenges_data['completed_challenges'])
        }
    
    def render_challenges_tab(self, language: str = 'en'):
        """Render the daily challenges tab."""
        translations = {
            'en': {
                'title': '🎯 Daily Challenges',
                'subtitle': 'Small steps toward better mental health',
                'difficulty': 'Challenge Difficulty:',
                'streak': 'Current Streak',
                'points': 'Total Points',
                'completed': 'Challenges Completed',
                'todays_challenge': "Today's Challenge",
                'instructions': 'Instructions:',
                'duration': 'Duration:',
                'points_reward': 'Points:',
                'complete_button': '✅ Mark as Complete',
                'completed_text': '🎉 Challenge Completed!',
                'next_challenge': 'Come back tomorrow for a new challenge!',
                'challenge_history': '📈 Challenge History',
                'no_history': 'Complete your first challenge to see history!',
                'beginner': 'Beginner',
                'intermediate': 'Intermediate', 
                'advanced': 'Advanced'
            },
            'hi': {
                'title': '🎯 दैनिक चुनौतियां',
                'subtitle': 'बेहतर मानसिक स्वास्थ्य की दिशा में छोटे कदम',
                'difficulty': 'चुनौती कठिनाई:',
                'streak': 'वर्तमान लक्ष्य',
                'points': 'कुल अंक',
                'completed': 'पूर्ण चुनौतियां',
                'todays_challenge': 'आज की चुनौती',
                'instructions': 'निर्देश:',
                'duration': 'अवधि:',
                'points_reward': 'अंक:',
                'complete_button': '✅ पूर्ण के रूप में चिह्नित करें',
                'completed_text': '🎉 चुनौती पूर्ण!',
                'next_challenge': 'नई चुनौती के लिए कल वापस आएं!',
                'challenge_history': '📈 चुनौती इतिहास',
                'no_history': 'इतिहास देखने के लिए अपनी पहली चुनौती पूरी करें!',
                'beginner': 'शुरुआती',
                'intermediate': 'मध्यम',
                'advanced': 'उन्नत'
            }
        }
        
        t = translations.get(language, translations['en'])
        
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(157, 78, 221, 0.1), rgba(58, 134, 255, 0.1)); border-radius: 20px; margin-bottom: 2rem;">
            <h1 style="color: #9D4EDD; font-size: 2.5rem; margin-bottom: 0.5rem;">{t['title']}</h1>
            <p style="color: #CCCCCC; font-size: 1.2rem;">{t['subtitle']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Difficulty selection
        col1, col2, col3 = st.columns(3)
        with col2:
            difficulty = st.selectbox(
                t['difficulty'],
                ['beginner', 'intermediate', 'advanced'],
                format_func=lambda x: t[x],
                key='challenge_difficulty'
            )
        
        # Stats display
        stats = self.get_streak_info()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                t['streak'],
                f"{stats['current_streak']} days",
                delta="🔥" if stats['current_streak'] > 0 else None
            )
        
        with col2:
            st.metric(
                t['points'],
                stats['total_points'],
                delta="💎"
            )
        
        with col3:
            st.metric(
                t['completed'],
                stats['total_completed'],
                delta="🏆"
            )
        
        st.markdown("---")
        
        # Today's challenge
        challenge = self.get_daily_challenge(difficulty)
        
        if challenge:
            st.subheader(t['todays_challenge'])
            
            # Challenge card
            completed = challenge.get('completed', False)
            card_color = 'rgba(57, 255, 20, 0.1)' if completed else 'rgba(157, 78, 221, 0.1)'
            border_color = 'rgba(57, 255, 20, 0.3)' if completed else 'rgba(157, 78, 221, 0.3)'
            
            st.markdown(f"""
            <div style="background: {card_color}; border: 2px solid {border_color}; border-radius: 15px; padding: 2rem; margin: 1rem 0;">
                <h3 style="color: #9D4EDD; margin-bottom: 1rem;">{challenge['title']}</h3>
                <p style="color: #FFFFFF; font-size: 1.1rem; margin-bottom: 1rem;">{challenge['description']}</p>
                <div style="background: rgba(0, 0, 0, 0.3); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong style="color: #39FF14;">{t['instructions']}</strong>
                    <p style="color: #CCCCCC; margin-top: 0.5rem;">{challenge['instructions']}</p>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                    <span style="color: #3A86FF;"><strong>{t['duration']}</strong> {challenge['duration']}</span>
                    <span style="color: #39FF14;"><strong>{t['points_reward']}</strong> {challenge['points']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Completion button
            if not completed:
                if st.button(t['complete_button'], type='primary', key='complete_challenge'):
                    if self.mark_challenge_complete(challenge):
                        st.success(t['completed_text'])
                        st.balloons()
                        st.rerun()
            else:
                st.success(t['completed_text'])
                st.info(t['next_challenge'])
        
        # Challenge history
        st.markdown("---")
        st.subheader(t['challenge_history'])
        
        if st.session_state.daily_challenges_data['challenge_history']:
            history = st.session_state.daily_challenges_data['challenge_history']
            
            for i, past_challenge in enumerate(reversed(history[-7:])):  # Show last 7 challenges
                date_str = past_challenge.get('completed_date', 'Unknown')
                st.markdown(f"""
                <div style="background: rgba(40, 40, 40, 0.8); border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #9D4EDD;">{past_challenge['title']}</strong>
                            <div style="color: #CCCCCC; font-size: 0.9rem;">{date_str}</div>
                        </div>
                        <div style="color: #39FF14; font-weight: bold;">+{past_challenge['points']} pts</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t['no_history'])
        
        # Back to Chatbot button
        st.markdown("---")
        if st.button("💬 Back to Chatbot", key="challenges_to_chat", type="secondary"):
            st.session_state.active_view = 'chat'
            st.rerun()