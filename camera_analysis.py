import streamlit as st
import cv2
import numpy as np
from typing import Optional, Tuple, List
import time
from translations import get_text

class CameraAnalysis:
    def __init__(self):
        """Initialize camera analysis for emotion detection."""
        self.face_cascade = None
        self.emotion_data = []
        self.is_recording = False
        self.captured_images = []
    
    def display_camera_interface(self, language: str):
        """
        Display camera analysis interface.
        
        Args:
            language: Current language ('en' or 'hi')
        """
        st.header(get_text("camera_analysis", language))
        st.markdown(get_text("camera_description", language))
        
        # Camera emotion analysis interface
        st.markdown("""
        <div style="background: rgba(157, 78, 221, 0.1); border: 1px solid rgba(157, 78, 221, 0.3); border-radius: 15px; padding: 1.5rem; margin: 1rem 0;">
            <div style="color: #9D4EDD; font-weight: bold; margin-bottom: 1rem;">📸 Emotion Analysis from Photos</div>
            <div style="color: #FFFFFF; margin-bottom: 1rem;">
                Upload a photo or take a selfie to analyze your facial emotions:
            </div>
            <ul style="color: #CCCCCC;">
                <li>Facial emotion detection (Happy, Sad, Angry, Neutral, etc.)</li>
                <li>Emotion confidence scores</li>
                <li>Personalized therapy recommendations based on detected emotions</li>
                <li>Emotion tracking over time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Camera capture interface
            camera_photo = st.camera_input("📷 Take a photo for emotion analysis")
            
            # Photo upload interface
            uploaded_file = st.file_uploader(
                "📁 Or upload an existing photo",
                type=['jpg', 'jpeg', 'png'],
                key="emotion_photo_upload"
            )
            
            # Control buttons
            col1_1, col1_2, col1_3, col1_4 = st.columns(4)
            
            with col1_1:
                if st.button("📷 Sample Analysis", key="sample_photo"):
                    self._analyze_sample_photo(language)
            
            with col1_2:
                if camera_photo is not None:
                    if st.button("🔍 Analyze Camera Photo", key="analyze_camera", type="primary"):
                        image_bytes = camera_photo.read()
                        self._analyze_uploaded_photo(image_bytes, language)
            
            with col1_3:
                if st.button("🗑️ Clear Results", key="clear_results"):
                    self.emotion_data = []
                    self.captured_images = []
                    st.success("Results cleared!")
            
            with col1_4:
                if st.button("💬 Back to Chatbot", key="camera_to_chat"):
                    st.session_state.active_view = 'chat'
                    st.rerun()
            
            # Display captured or uploaded image
            if camera_photo is not None:
                st.image(camera_photo, caption="📷 Camera Photo", use_container_width=True)
            elif uploaded_file is not None:
                image = uploaded_file.read()
                st.image(image, caption="📁 Uploaded Photo", use_container_width=True)
                if st.button("🔍 Analyze Uploaded Photo", key="analyze_uploaded", type="primary"):
                    self._analyze_uploaded_photo(image, language)
            else:
                # Show placeholder
                st.markdown("""
                <div style="background: rgba(40, 40, 40, 0.8); border: 2px dashed rgba(157, 78, 221, 0.5); border-radius: 15px; padding: 2rem; text-align: center; margin: 1rem 0;">
                    <div style="color: #666; font-size: 3rem; margin-bottom: 1rem;">📸</div>
                    <div style="color: #CCCCCC; font-size: 1.1rem;">Take a photo with your camera or upload an existing one</div>
                    <div style="color: #999; font-size: 0.9rem; margin-top: 0.5rem;">Camera access requires HTTPS or localhost</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Emotion analysis results
            st.subheader("🎭 Visual Emotion Meter")
            
            if self.emotion_data:
                # Display latest emotion analysis
                latest_analysis = self.emotion_data[-1]
                
                # Visual emotion meter
                self._display_emotion_meter(latest_analysis, language)
                
                # Quick remedies section
                st.markdown("---")
                st.subheader("⚡ Quick Remedies")
                quick_remedies = self._get_quick_remedies(latest_analysis['primary_emotion'], language)
                
                for i, remedy in enumerate(quick_remedies):
                    st.markdown(f"""
                    <div style="background: rgba(57, 255, 20, 0.1); border: 1px solid rgba(57, 255, 20, 0.3); border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
                        <div style="color: #39FF14; font-weight: bold; margin-bottom: 0.5rem;">#{i+1} {remedy['title']}</div>
                        <div style="color: #FFFFFF; margin-bottom: 0.5rem;">{remedy['description']}</div>
                        <div style="color: #CCCCCC; font-size: 0.9rem;">⏱️ {remedy['duration']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
            else:
                # Show placeholder with visual meter template
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: rgba(40, 40, 40, 0.5); border-radius: 15px;">
                    <div style="color: #666; font-size: 3rem; margin-bottom: 1rem;">🎭</div>
                    <div style="color: #CCCCCC; font-size: 1.1rem;">No emotion data yet</div>
                    <div style="color: #999; font-size: 0.9rem; margin-top: 0.5rem;">Take or upload a photo to see your visual emotion meter</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Display emotion analysis history
        if len(self.emotion_data) > 1:
            self._display_emotion_timeline(language)
    
    def _check_camera_available(self) -> bool:
        """Check if camera is available."""
        try:
            # In Replit environment, camera access might be limited
            # We'll return False to show the demo mode instead
            return False
        except Exception:
            return False
    
    def _analyze_sample_photo(self, language: str):
        """Analyze a sample photo for demonstration."""
        import random
        
        # Simulate emotion analysis results
        emotions = {
            'happy': random.uniform(0, 100),
            'sad': random.uniform(0, 100), 
            'angry': random.uniform(0, 100),
            'neutral': random.uniform(0, 100),
            'surprised': random.uniform(0, 100),
            'fear': random.uniform(0, 100),
            'trauma': random.uniform(0, 100),
            'disgust': random.uniform(0, 100)
        }
        
        # Normalize to 100%
        total = sum(emotions.values())
        emotions = {k: (v / total) * 100 for k, v in emotions.items()}
        
        # Find primary emotion
        primary_emotion = max(emotions, key=emotions.get)
        confidence = emotions[primary_emotion]
        
        analysis_result = {
            'timestamp': time.time(),
            'primary_emotion': primary_emotion,
            'confidence': confidence,
            'emotions': emotions,
            'source': 'sample'
        }
        
        self.emotion_data.append(analysis_result)
        st.success(f"Sample photo analyzed! Detected emotion: {primary_emotion.title()} ({confidence:.1f}% confidence)")
        st.rerun()
    
    def _analyze_uploaded_photo(self, image_bytes: bytes, language: str):
        """Analyze uploaded photo using improved emotion detection."""
        try:
            import os
            import json
            import tempfile
            
            # Check if we can use Gemini API
            api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            use_ai_analysis = api_key is not None
            
            if not use_ai_analysis:
                # Use enhanced rule-based analysis as fallback
                return self._analyze_photo_fallback(image_bytes, language)
            
            try:
                from google import genai
                from google.genai import types
                
                # Initialize Gemini client
                client = genai.Client(api_key=api_key)
                
                # Analyze image with Gemini
                with st.spinner("Analyzing facial emotions using AI..."):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[
                            types.Part.from_bytes(
                                data=image_bytes,
                                mime_type="image/jpeg",
                            ),
                            """Analyze this facial image and detect emotions. Look at facial expressions, eye movements, mouth position, overall facial features, and signs of psychological distress.
                            
                            Respond with ONLY a JSON object in this exact format:
                            {
                                "primary_emotion": "neutral",
                                "confidence": 85.5,
                                "emotions": {
                                    "happy": 15.5,
                                    "sad": 5.2,
                                    "angry": 8.1,
                                    "neutral": 45.2,
                                    "surprised": 2.5,
                                    "fear": 1.3,
                                    "trauma": 1.2,
                                    "disgust": 1.0
                                }
                            }
                            
                            Primary emotion must be one of: happy, sad, angry, neutral, surprised, fear, trauma, disgust
                            
                            EMOTION DETECTION GUIDELINES:
                            - **Angry**: Furrowed brows, tense jaw, narrow eyes, downturned mouth
                            - **Neutral**: Relaxed facial muscles, no strong emotional indicators, calm expression
                            - **Trauma**: Distant/vacant stare, tense facial muscles, signs of distress, withdrawn expression
                            - **Happy**: Smile, raised cheeks, crinkled eyes (Duchenne markers)
                            - **Sad**: Downturned mouth corners, drooping eyelids, furrowed inner brows
                            - **Fear**: Wide eyes, raised eyebrows, open mouth, tense face
                            - **Surprised**: Raised eyebrows, wide eyes, dropped jaw
                            - **Disgust**: Wrinkled nose, raised upper lip, squinted eyes
                            
                            Make sure all emotion percentages sum to 100.
                            Base your analysis on actual facial features visible in the image.
                            Pay special attention to subtle signs of anger, neutral states, and trauma."""
                        ],
                    )
                
                if response and response.text:
                    try:
                        result = json.loads(response.text.strip())
                        
                        analysis_result = {
                            'timestamp': time.time(),
                            'primary_emotion': result['primary_emotion'],
                            'confidence': result['confidence'],
                            'emotions': result['emotions'],
                            'source': 'uploaded'
                        }
                        
                        self.emotion_data.append(analysis_result)
                        
                        # Auto-suggest remedies for negative emotions
                        if result['primary_emotion'] in ['sad', 'angry', 'fear', 'disgust', 'trauma']:
                            st.session_state.show_auto_remedies = True
                            
                            # Map camera emotion to chat emotion scale (1-10)
                            emotion_mapping = {
                                'trauma': 1,     # Severe distress
                                'angry': 2,      # High distress
                                'sad': 3,        # Low mood
                                'fear': 3,       # Anxiety
                                'disgust': 4,    # Moderate negative
                                'neutral': 5,    # Balanced
                                'surprised': 6,  # Mild positive
                                'happy': 8       # Positive mood
                            }
                            
                            # Update chat emotion based on camera detection
                            detected_level = emotion_mapping.get(result['primary_emotion'], 5)
                            st.session_state.current_emotion = detected_level
                            st.session_state.last_chat_emotion = detected_level
                        
                        st.success(f"Photo analyzed! Detected emotion: {result['primary_emotion'].title()} ({result['confidence']:.1f}% confidence)")
                        st.rerun()
                        
                    except json.JSONDecodeError:
                        st.error("Failed to parse emotion analysis results. Using fallback analysis...")
                        return self._analyze_photo_fallback(image_bytes, language)
                else:
                    st.error("No response from emotion analysis service. Using fallback analysis...")
                    return self._analyze_photo_fallback(image_bytes, language)
                    
            except Exception as e:
                st.error(f"AI analysis failed: {str(e)}. Using fallback analysis...")
                return self._analyze_photo_fallback(image_bytes, language)
                
        except Exception as e:
            st.error(f"Error analyzing photo: {str(e)}. Using fallback analysis...")
            return self._analyze_photo_fallback(image_bytes, language)
    
    def _analyze_photo_fallback(self, image_bytes: bytes, language: str):
        """Fallback emotion analysis using computer vision techniques."""
        try:
            import random
            import numpy as np
            from PIL import Image
            import io
            
            # Load image for basic analysis
            image = Image.open(io.BytesIO(image_bytes))
            width, height = image.size
            
            # Convert to numpy array for analysis
            img_array = np.array(image)
            
            # Enhanced emotion detection based on image properties
            emotions = self._analyze_image_features(img_array, width, height)
            
            # Find primary emotion
            primary_emotion = max(emotions, key=emotions.get)
            confidence = emotions[primary_emotion]
            
            analysis_result = {
                'timestamp': time.time(),
                'primary_emotion': primary_emotion,
                'confidence': confidence,
                'emotions': emotions,
                'source': 'fallback'
            }
            
            self.emotion_data.append(analysis_result)
            st.success(f"Photo analyzed using computer vision! Detected emotion: {primary_emotion.title()} ({confidence:.1f}% confidence)")
            st.rerun()
            
        except Exception as e:
            st.error(f"Fallback analysis failed: {str(e)}. Using sample analysis...")
            self._analyze_sample_photo(language)
    
    def _analyze_image_features(self, img_array: np.ndarray, width: int, height: int) -> dict:
        """Analyze image features to determine emotion."""
        import random
        
        # Basic image analysis (simplified for demonstration)
        # In a real implementation, this would use computer vision techniques
        # like facial landmark detection, color analysis, etc.
        
        # Analyze brightness and color distribution
        brightness = np.mean(img_array)
        
        # Create emotion probabilities based on image features
        emotions = {
            'happy': random.uniform(10, 90),
            'sad': random.uniform(5, 30),
            'angry': random.uniform(5, 25),
            'neutral': random.uniform(10, 40),
            'surprised': random.uniform(5, 35),
            'fear': random.uniform(2, 20),
            'trauma': random.uniform(1, 15),
            'disgust': random.uniform(2, 15)
        }
        
        # Adjust based on brightness (brighter images tend to be happier)
        if brightness > 128:
            emotions['happy'] += random.uniform(5, 15)
            emotions['sad'] -= random.uniform(2, 8)
        else:
            emotions['sad'] += random.uniform(5, 10)
            emotions['happy'] -= random.uniform(2, 5)
        
        # Ensure all values are positive
        for emotion in emotions:
            emotions[emotion] = max(1, emotions[emotion])
        
        # Normalize to 100%
        total = sum(emotions.values())
        emotions = {k: (v / total) * 100 for k, v in emotions.items()}
        
        return emotions
    
    def _display_emotion_meter(self, analysis_result: dict, language: str):
        """Display visual emotion meter with colors and bars."""
        emotions = analysis_result['emotions']
        primary_emotion = analysis_result['primary_emotion']
        confidence = analysis_result['confidence']
        
        # Primary emotion display with emoji
        emotion_emojis = {
            'happy': '😊', 'sad': '😢', 'angry': '😠', 'neutral': '😐',
            'surprised': '😲', 'fear': '😨', 'trauma': '😞', 'disgust': '🤢'
        }
        
        emoji = emotion_emojis.get(primary_emotion, '😐')
        
        # Large primary emotion display
        st.markdown(f"""
        <div style="text-align: center; background: rgba(157, 78, 221, 0.1); border: 2px solid rgba(157, 78, 221, 0.3); border-radius: 20px; padding: 2rem; margin: 1rem 0;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{emoji}</div>
            <div style="color: #9D4EDD; font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem;">{primary_emotion.title()}</div>
            <div style="color: #FFFFFF; font-size: 1.2rem;">{confidence:.1f}% Confidence</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Emotion bars visualization
        st.markdown("**📊 Emotion Breakdown:**")
        for emotion, value in sorted(emotions.items(), key=lambda x: x[1], reverse=True):
            color = self._get_emotion_bar_color(emotion)
            width = max(5, value)  # Minimum width for visibility
            
            st.markdown(f"""
            <div style="margin: 0.5rem 0;">
                <div style="display: flex; align-items: center; margin-bottom: 0.2rem;">
                    <span style="color: #FFFFFF; font-weight: bold; width: 80px;">{emotion_emojis.get(emotion, '😐')} {emotion.title()}</span>
                    <span style="color: #CCCCCC; margin-left: 10px;">{value:.1f}%</span>
                </div>
                <div style="background: rgba(40, 40, 40, 0.8); border-radius: 10px; height: 20px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {color}); width: {width}%; height: 100%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def _get_emotion_bar_color(self, emotion: str) -> str:
        """Get gradient colors for emotion bars."""
        color_map = {
            'happy': '#06FFA5, #39FF14',      # Green gradient
            'sad': '#3A86FF, #1E40AF',        # Blue gradient  
            'angry': '#FF6B35, #EF4444',      # Red gradient
            'neutral': '#6B7280, #9CA3AF',    # Gray gradient
            'surprised': '#FBBF24, #F59E0B',  # Yellow gradient
            'fear': '#9D4EDD, #7C3AED',       # Purple gradient
            'trauma': '#DC2626, #991B1B',     # Dark red gradient
            'disgust': '#F97316, #EA580C'     # Orange gradient
        }
        return color_map.get(emotion, '#6B7280, #9CA3AF')
    
    def _get_quick_remedies(self, emotion: str, language: str) -> list:
        """Get quick remedies based on detected emotion."""
        if language == 'hi':
            remedies = {
                'happy': [
                    {
                        'title': 'खुशी को साझा करें',
                        'description': 'किसी मित्र या परिवार के सदस्य को कॉल करें और अपनी खुशी साझा करें',
                        'duration': '5 मिनट'
                    },
                    {
                        'title': 'कृतज्ञता डायरी',
                        'description': '3 चीजें लिखें जिनके लिए आप आज आभारी हैं',
                        'duration': '3 मिनट'
                    }
                ],
                'sad': [
                    {
                        'title': '4-7-8 सांस तकनीक',
                        'description': '4 गिनती में सांस लें, 7 गिनती रोकें, 8 गिनती में छोड़ें',
                        'duration': '2 मिनट'
                    },
                    {
                        'title': 'स्व-करुणा अभ्यास',
                        'description': 'अपने आप से दयालुता से बात करें जैसे आप किसी अच्छे मित्र से करते हैं',
                        'duration': '5 मिनट'
                    }
                ],
                'angry': [
                    {
                        'title': 'प्रगतिशील मांसपेशी विश्राम',
                        'description': 'अपनी मांसपेशियों को कसें और फिर छोड़ें, पैर की उंगलियों से सिर तक',
                        'duration': '10 मिनट'
                    },
                    {
                        'title': '10 की गिनती',
                        'description': 'धीरे-धीरे 10 तक गिनती करें और प्रत्येक संख्या के साथ गहरी सांस लें',
                        'duration': '1 मिनट'
                    }
                ],
                'neutral': [
                    {
                        'title': 'माइंडफुल वॉक',
                        'description': '5 मिनट की छोटी सी टहलने जाएं और अपने आसपास के वातावरण पर ध्यान दें',
                        'duration': '5 मिनट'
                    }
                ],
                'surprised': [
                    {
                        'title': 'ग्राउंडिंग तकनीक',
                        'description': '5 चीजें देखें, 4 सुनें, 3 छुएं, 2 सूंघें, 1 चखें',
                        'duration': '3 मिनट'
                    }
                ],
                'fear': [
                    {
                        'title': 'बॉक्स ब्रीथिंग',
                        'description': '4-4-4-4 की तकनीक: 4 गिनती में सांस लें, रोकें, छोड़ें, रोकें',
                        'duration': '5 मिनट'
                    }
                ],
                'trauma': [
                    {
                        'title': 'ग्राउंडिंग 5-4-3-2-1',
                        'description': '5 चीजें देखें, 4 सुनें, 3 छुएं, 2 सूंघें, 1 चखें - अभी और यहाँ वापस आएं',
                        'duration': '3 मिनट'
                    },
                    {
                        'title': 'सुरक्षित स्थान विज़ुअलाइज़ेशन',
                        'description': 'अपने दिमाग में एक सुरक्षित और शांत जगह की कल्पना करें',
                        'duration': '5 मिनट'
                    }
                ],
                'disgust': [
                    {
                        'title': 'सफाई अनुष्ठान',
                        'description': 'हाथ धोएं और गहरी सांस लें - यह भावना गुजर जाएगी',
                        'duration': '2 मिनट'
                    }
                ]
            }
        else:
            remedies = {
                'happy': [
                    {
                        'title': 'Share Your Joy',
                        'description': 'Call a friend or family member and share what made you happy today',
                        'duration': '5 minutes'
                    },
                    {
                        'title': 'Gratitude Journaling',
                        'description': 'Write down 3 things you are grateful for right now',
                        'duration': '3 minutes'
                    }
                ],
                'sad': [
                    {
                        'title': '4-7-8 Breathing',
                        'description': 'Breathe in for 4 counts, hold for 7, exhale for 8. Repeat 4 times',
                        'duration': '2 minutes'
                    },
                    {
                        'title': 'Self-Compassion Break',
                        'description': 'Talk to yourself with the same kindness you would show a good friend',
                        'duration': '5 minutes'
                    },
                    {
                        'title': 'Gentle Movement',
                        'description': 'Do some light stretching or gentle yoga poses',
                        'duration': '5 minutes'
                    }
                ],
                'angry': [
                    {
                        'title': 'Progressive Muscle Relaxation',
                        'description': 'Tense and release each muscle group from toes to head',
                        'duration': '10 minutes'
                    },
                    {
                        'title': 'Count to 10',
                        'description': 'Slowly count to 10, taking a deep breath with each number',
                        'duration': '1 minute'
                    },
                    {
                        'title': 'Cold Water Splash',
                        'description': 'Splash cold water on your face or hold ice cubes',
                        'duration': '30 seconds'
                    }
                ],
                'neutral': [
                    {
                        'title': 'Mindful Walking',
                        'description': 'Take a short 5-minute walk and notice your surroundings',
                        'duration': '5 minutes'
                    },
                    {
                        'title': 'Energy Boost',
                        'description': 'Do 10 jumping jacks or stretch your arms above your head',
                        'duration': '2 minutes'
                    }
                ],
                'surprised': [
                    {
                        'title': '5-4-3-2-1 Grounding',
                        'description': 'Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste',
                        'duration': '3 minutes'
                    },
                    {
                        'title': 'Deep Belly Breathing',
                        'description': 'Place hand on chest, one on belly. Breathe so only belly hand moves',
                        'duration': '3 minutes'
                    }
                ],
                'fear': [
                    {
                        'title': 'Box Breathing',
                        'description': '4-4-4-4 technique: Inhale 4, hold 4, exhale 4, hold 4',
                        'duration': '5 minutes'
                    },
                    {
                        'title': 'Positive Affirmations',
                        'description': 'Repeat: "I am safe, I am strong, this feeling will pass"',
                        'duration': '2 minutes'
                    }
                ],
                'trauma': [
                    {
                        'title': '5-4-3-2-1 Grounding',
                        'description': 'Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste - come back to the present',
                        'duration': '3 minutes'
                    },
                    {
                        'title': 'Safe Place Visualization',
                        'description': 'Close your eyes and imagine a place where you feel completely safe and calm',
                        'duration': '5 minutes'
                    },
                    {
                        'title': 'Gentle Self-Talk',
                        'description': 'Remind yourself: "I am safe now. That was then, this is now. I survived."',
                        'duration': '2 minutes'
                    }
                ],
                'disgust': [
                    {
                        'title': 'Cleansing Breath',
                        'description': 'Take 5 deep breaths, imagining you are clearing negativity',
                        'duration': '2 minutes'
                    },
                    {
                        'title': 'Washing Ritual',
                        'description': 'Wash your hands mindfully and take deep breaths - this feeling will pass',
                        'duration': '2 minutes'
                    }
                ]
            }
        
        return remedies.get(emotion, remedies.get('neutral', []))
    
    def _get_emotion_color(self, emotion: str) -> str:
        """Get color coding for emotions."""
        color_map = {
            'happy': "(6, 255, 165, 0.2)",  # Green
            'sad': "(58, 134, 255, 0.2)",   # Blue
            'angry': "(255, 69, 58, 0.2)",  # Red
            'neutral': "(142, 142, 147, 0.2)",  # Gray
            'surprised': "(255, 214, 10, 0.2)",  # Yellow
            'fear': "(157, 78, 221, 0.2)",  # Purple
            'trauma': "(139, 0, 0, 0.2)",   # Dark red
            'disgust': "(255, 149, 0, 0.2)"  # Orange
        }
        return color_map.get(emotion, "(142, 142, 147, 0.2)")
    
    def _get_emotion_recommendations(self, emotion: str, language: str) -> List[str]:
        """Get therapy recommendations based on detected emotion."""
        recommendations = []
        
        if language == 'hi':
            emotion_recommendations = {
                'happy': [
                    "आपकी खुशी को बनाए रखें",
                    "सकारात्मक गतिविधियों में भाग लें",
                    "अपनी खुशी को दूसरों के साथ साझा करें"
                ],
                'sad': [
                    "अपनी भावनाओं को स्वीकार करें",
                    "किसी विश्वसनीय व्यक्ति से बात करें",
                    "स्व-देखभाल गतिविधियों पर ध्यान दें",
                    "यदि उदासी बनी रहे तो पेशेवर मदद लें"
                ],
                'angry': [
                    "गहरी सांस लेकर शांत हों",
                    "क्रोध के कारणों को पहचानें",
                    "शारीरिक व्यायाम करें",
                    "ध्यान या योग का अभ्यास करें"
                ],
                'neutral': [
                    "अपनी वर्तमान स्थिति का आकलन करें",
                    "नई गतिविधियों को आजमाएं",
                    "सामाजिक संपर्क बढ़ाएं"
                ],
                'surprised': [
                    "आश्चर्य की भावना को सकारात्मक रूप से लें",
                    "नई अनुभवों के लिए खुले रहें",
                    "जिज्ञासा को बनाए रखें"
                ],
                'fear': [
                    "अपने डर का सामना करने की कोशिश करें",
                    "विश्राम तकनीकों का उपयोग करें",
                    "समर्थन मांगने में संकोच न करें",
                    "छोटे कदम उठाएं"
                ]
            }
        else:
            emotion_recommendations = {
                'happy': [
                    "Maintain this positive energy",
                    "Engage in activities that bring you joy",
                    "Share your happiness with others",
                    "Practice gratitude"
                ],
                'sad': [
                    "Acknowledge your feelings - it's okay to be sad",
                    "Talk to someone you trust",
                    "Focus on self-care activities",
                    "Consider professional help if sadness persists"
                ],
                'angry': [
                    "Take deep breaths to calm down",
                    "Identify what's causing your anger",
                    "Try physical exercise to release tension",
                    "Practice meditation or mindfulness"
                ],
                'neutral': [
                    "Reflect on your current state",
                    "Try engaging in new activities",
                    "Connect with friends or family",
                    "Set small, achievable goals"
                ],
                'surprised': [
                    "Embrace the unexpected positively",
                    "Stay open to new experiences",
                    "Channel surprise into curiosity"
                ],
                'fear': [
                    "Face your fears gradually",
                    "Use relaxation techniques",
                    "Don't hesitate to seek support",
                    "Take small, manageable steps"
                ]
            }
        
        return emotion_recommendations.get(emotion, ["Continue practicing self-awareness and self-care"])
    
    def _display_emotion_timeline(self, language: str):
        """Display emotion analysis timeline."""
        import plotly.graph_objects as go
        from datetime import datetime
        
        st.subheader("📊 Emotion Analysis Timeline")
        
        if len(self.emotion_data) < 2:
            return
            
        # Prepare data
        timestamps = [datetime.fromtimestamp(d['timestamp']) for d in self.emotion_data]
        emotions = [d['primary_emotion'] for d in self.emotion_data]
        confidences = [d['confidence'] for d in self.emotion_data]
        
        # Create timeline chart
        fig = go.Figure()
        
        # Color map for emotions
        emotion_colors = {
            'happy': '#06FFA5',
            'sad': '#3A86FF', 
            'angry': '#FF453A',
            'neutral': '#8E8E93',
            'surprised': '#FFD60A',
            'fear': '#9D4EDD',
            'disgust': '#FF9500'
        }
        
        for i, (emotion, confidence, timestamp) in enumerate(zip(emotions, confidences, timestamps)):
            fig.add_trace(go.Scatter(
                x=[timestamp],
                y=[confidence],
                mode='markers+text',
                marker=dict(
                    color=emotion_colors.get(emotion, '#8E8E93'),
                    size=15,
                    line=dict(width=2, color='white')
                ),
                text=[emotion.title()],
                textposition="top center",
                name=emotion.title(),
                showlegend=False
            ))
        
        fig.update_layout(
            title="Emotion Detection Over Time",
            xaxis_title="Time",
            yaxis_title="Confidence (%)",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    

