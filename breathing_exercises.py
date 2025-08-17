import streamlit as st
import time
import threading
from typing import Dict
from translations import get_text

class BreathingExercises:
    def __init__(self):
        """Initialize breathing exercises."""
        self.exercises = {
            'en': {
                '4-7-8': {
                    'name': '4-7-8 Breathing',
                    'description': 'Inhale for 4, hold for 7, exhale for 8 seconds',
                    'steps': ['Inhale', 'Hold', 'Exhale'],
                    'durations': [4, 7, 8],
                    'benefits': 'Reduces anxiety and promotes sleep'
                },
                'box': {
                    'name': 'Box Breathing',
                    'description': 'Inhale, hold, exhale, hold - each for 4 seconds',
                    'steps': ['Inhale', 'Hold', 'Exhale', 'Hold'],
                    'durations': [4, 4, 4, 4],
                    'benefits': 'Improves focus and reduces stress'
                },
                'triangle': {
                    'name': 'Triangle Breathing',
                    'description': 'Inhale for 4, hold for 4, exhale for 4 seconds',
                    'steps': ['Inhale', 'Hold', 'Exhale'],
                    'durations': [4, 4, 4],
                    'benefits': 'Simple technique for beginners'
                }
            },
            'hi': {
                '4-7-8': {
                    'name': '4-7-8 सांस लेना',
                    'description': '4 सेकंड सांस लें, 7 सेकंड रोकें, 8 सेकंड छोड़ें',
                    'steps': ['सांस लें', 'रोकें', 'छोड़ें'],
                    'durations': [4, 7, 8],
                    'benefits': 'चिंता कम करता है और नींद में सहायक है'
                },
                'box': {
                    'name': 'बॉक्स ब्रीदिंग',
                    'description': 'सांस लें, रोकें, छोड़ें, रोकें - हर एक 4 सेकंड के लिए',
                    'steps': ['सांस लें', 'रोकें', 'छोड़ें', 'रोकें'],
                    'durations': [4, 4, 4, 4],
                    'benefits': 'फोकस बढ़ाता है और तनाव कम करता है'
                },
                'triangle': {
                    'name': 'त्रिकोण सांस',
                    'description': '4 सेकंड सांस लें, 4 सेकंड रोकें, 4 सेकंड छोड़ें',
                    'steps': ['सांस लें', 'रोकें', 'छोड़ें'],
                    'durations': [4, 4, 4],
                    'benefits': 'शुरुआती लोगों के लिए सरल तकनीक'
                }
            }
        }
    
    def display_breathing_interface(self, language: str):
        """
        Display breathing exercises interface.
        
        Args:
            language: Current language ('en' or 'hi')
        """
        st.header(get_text("breathing_exercises", language))
        st.markdown(get_text("breathing_description", language))
        
        # Exercise selection
        exercise_options = list(self.exercises[language].keys())
        exercise_names = [self.exercises[language][key]['name'] for key in exercise_options]
        
        selected_exercise_name = st.selectbox(
            get_text("select_exercise", language),
            exercise_names
        )
        
        # Find selected exercise key
        selected_exercise = None
        for key, exercise in self.exercises[language].items():
            if exercise['name'] == selected_exercise_name:
                selected_exercise = key
                break
        
        if selected_exercise:
            exercise_data = self.exercises[language][selected_exercise]
            
            # Display exercise info
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader(exercise_data['name'])
                st.write(f"**{get_text('description', language)}:** {exercise_data['description']}")
                st.write(f"**{get_text('benefits', language)}:** {exercise_data['benefits']}")
                
            with col2:
                # Exercise settings
                st.subheader(get_text("settings", language))
                rounds = st.number_input(
                    get_text("number_of_rounds", language),
                    min_value=1,
                    max_value=20,
                    value=5
                )
                
                # Control buttons
                if st.button(get_text("start_exercise", language), type="primary", key="start_breathing"):
                    self._run_breathing_exercise(exercise_data, rounds, language)
                if st.button("💬 Back to Chatbot", key="breathing_to_chat"):
                    st.session_state.active_view = 'chat'
                    st.rerun()
            
            # Visual guide
            st.subheader(get_text("visual_guide", language))
            self._display_breathing_visual(selected_exercise, language)
            
            # Tips section
            st.subheader(get_text("breathing_tips", language))
            tips = self._get_breathing_tips(language)
            for tip in tips:
                st.write(f"• {tip}")
    
    def _run_breathing_exercise(self, exercise_data: Dict, rounds: int, language: str):
        """
        Run the selected breathing exercise with visual cues.
        
        Args:
            exercise_data: Exercise configuration
            rounds: Number of rounds to perform
            language: Current language
        """
        st.subheader(get_text("exercise_in_progress", language))
        
        # Create placeholders
        instruction_placeholder = st.empty()
        progress_placeholder = st.empty()
        timer_placeholder = st.empty()
        circle_placeholder = st.empty()
        
        try:
            for round_num in range(1, rounds + 1):
                # Round indicator
                progress_placeholder.progress(round_num / rounds)
                st.write(f"{get_text('round', language)} {round_num}/{rounds}")
                
                for step_idx, (step, duration) in enumerate(zip(exercise_data['steps'], exercise_data['durations'])):
                    # Display instruction
                    instruction_placeholder.markdown(f"## {step}")
                    
                    # Visual breathing circle with neon colors
                    if step == exercise_data['steps'][0]:  # Inhale
                        circle_size = "transform: scale(1.5);"
                        circle_color = "#39FF14"  # Neon green
                    elif step == exercise_data['steps'][-1]:  # Exhale
                        circle_size = "transform: scale(0.5);"
                        circle_color = "#3A86FF"  # Neon blue
                    else:  # Hold
                        circle_size = "transform: scale(1.0);"
                        circle_color = "#9D4EDD"  # Neon purple
                    
                    circle_placeholder.markdown(
                        f"""
                        <div style="
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 200px;
                        ">
                            <div style="
                                width: 100px;
                                height: 100px;
                                border-radius: 50%;
                                background-color: {circle_color};
                                {circle_size}
                                transition: all {duration}s ease-in-out;
                                opacity: 0.7;
                            "></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Countdown timer
                    for remaining in range(duration, 0, -1):
                        timer_placeholder.markdown(f"### {remaining}")
                        time.sleep(1)
                
                # Brief pause between rounds
                if round_num < rounds:
                    instruction_placeholder.markdown(f"## {get_text('rest', language)}")
                    time.sleep(2)
            
            # Exercise completed
            instruction_placeholder.success(get_text("exercise_completed", language))
            timer_placeholder.empty()
            circle_placeholder.empty()
            
            # Show completion message
            st.balloons()
            st.success(get_text("well_done", language))
            
        except Exception as e:
            st.error(f"{get_text('exercise_error', language)}: {str(e)}")
    
    def _display_breathing_visual(self, exercise_type: str, language: str):
        """Display visual breathing guide."""
        if exercise_type == '4-7-8':
            st.markdown(
                """
                <div style="text-align: center;">
                    <div style="display: inline-block; margin: 10px;">
                        <div style="width: 60px; height: 60px; border-radius: 50%; background-color: #39FF14; display: flex; align-items: center; justify-content: center; color: #000; font-weight: bold; box-shadow: 0 0 15px rgba(57, 255, 20, 0.6);">4s</div>
                        <p style="color: #39FF14;">Inhale / सांस लें</p>
                    </div>
                    <span style="font-size: 24px; margin: 0 20px; color: #9D4EDD;">→</span>
                    <div style="display: inline-block; margin: 10px;">
                        <div style="width: 60px; height: 60px; border-radius: 50%; background-color: #9D4EDD; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; box-shadow: 0 0 15px rgba(157, 78, 221, 0.6);">7s</div>
                        <p style="color: #9D4EDD;">Hold / रोकें</p>
                    </div>
                    <span style="font-size: 24px; margin: 0 20px; color: #9D4EDD;">→</span>
                    <div style="display: inline-block; margin: 10px;">
                        <div style="width: 60px; height: 60px; border-radius: 50%; background-color: #3A86FF; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; box-shadow: 0 0 15px rgba(58, 134, 255, 0.6);">8s</div>
                        <p style="color: #3A86FF;">Exhale / छोड़ें</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif exercise_type == 'box':
            st.markdown(
                """
                <div style="text-align: center;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 300px; margin: 0 auto;">
                        <div style="background-color: #4CAF50; padding: 20px; color: white; text-align: center; border-radius: 10px;">
                            <strong>4s</strong><br>Inhale<br>सांस लें
                        </div>
                        <div style="background-color: #FF9800; padding: 20px; color: white; text-align: center; border-radius: 10px;">
                            <strong>4s</strong><br>Hold<br>रोकें
                        </div>
                        <div style="background-color: #2196F3; padding: 20px; color: white; text-align: center; border-radius: 10px;">
                            <strong>4s</strong><br>Exhale<br>छोड़ें
                        </div>
                        <div style="background-color: #9C27B0; padding: 20px; color: white; text-align: center; border-radius: 10px;">
                            <strong>4s</strong><br>Hold<br>रोकें
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:  # triangle
            st.markdown(
                """
                <div style="text-align: center;">
                    <div style="position: relative; width: 200px; height: 200px; margin: 0 auto;">
                        <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); background-color: #4CAF50; padding: 10px; border-radius: 50%; color: white;">
                            <strong>4s</strong><br>Inhale<br>सांस लें
                        </div>
                        <div style="position: absolute; bottom: 0; left: 0; background-color: #FF9800; padding: 10px; border-radius: 50%; color: white;">
                            <strong>4s</strong><br>Hold<br>रोकें
                        </div>
                        <div style="position: absolute; bottom: 0; right: 0; background-color: #2196F3; padding: 10px; border-radius: 50%; color: white;">
                            <strong>4s</strong><br>Exhale<br>छोड़ें
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    def _get_breathing_tips(self, language: str) -> list:
        """Get breathing exercise tips."""
        if language == 'hi':
            return [
                "एक आरामदायक स्थिति में बैठें या लेटें",
                "अपनी आंखें बंद करें या एक बिंदु पर ध्यान दें",
                "नाक से सांस लें और मुंह से छोड़ें",
                "अपने पेट को सांस के साथ फूलने दें",
                "यदि चक्कर आए तो तुरंत रुकें",
                "नियमित अभ्यास से बेहतर परिणाम मिलते हैं",
                "शुरुआत में कम राउंड करें"
            ]
        else:
            return [
                "Sit or lie down in a comfortable position",
                "Close your eyes or focus on a single point",
                "Breathe in through your nose and out through your mouth",
                "Allow your belly to expand with each breath",
                "Stop immediately if you feel dizzy",
                "Regular practice yields better results",
                "Start with fewer rounds as a beginner"
            ]
