import streamlit as st
import random
from typing import List, Dict
from translations import get_text

class QuickRemedies:
    def __init__(self):
        """Initialize quick remedies system."""
        self.remedies = {
            'en': {
                'anxiety': [
                    {
                        'title': '5-4-3-2-1 Grounding Technique',
                        'description': 'Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.',
                        'duration': '2-3 minutes',
                        'category': 'grounding'
                    },
                    {
                        'title': 'Progressive Muscle Relaxation',
                        'description': 'Tense and relax each muscle group starting from your toes to your head.',
                        'duration': '10-15 minutes',
                        'category': 'relaxation'
                    },
                    {
                        'title': 'Cold Water on Face',
                        'description': 'Splash cold water on your face or hold ice cubes to activate the diving response.',
                        'duration': '1-2 minutes',
                        'category': 'physical'
                    }
                ],
                'stress': [
                    {
                        'title': 'Box Breathing',
                        'description': 'Breathe in for 4 counts, hold for 4, exhale for 4, hold for 4. Repeat.',
                        'duration': '5-10 minutes',
                        'category': 'breathing'
                    },
                    {
                        'title': 'Quick Walk',
                        'description': 'Take a 5-minute walk, focusing on your surroundings and breathing.',
                        'duration': '5 minutes',
                        'category': 'physical'
                    },
                    {
                        'title': 'Positive Affirmations',
                        'description': 'Repeat: "I am capable, I am strong, I can handle this situation."',
                        'duration': '2-3 minutes',
                        'category': 'mental'
                    }
                ],
                'sadness': [
                    {
                        'title': 'Gratitude List',
                        'description': 'Write down 3 things you are grateful for today, no matter how small.',
                        'duration': '5 minutes',
                        'category': 'mental'
                    },
                    {
                        'title': 'Gentle Movement',
                        'description': 'Do some light stretching or gentle yoga poses to release tension.',
                        'duration': '10 minutes',
                        'category': 'physical'
                    },
                    {
                        'title': 'Connect with Someone',
                        'description': 'Call or message a friend, family member, or support person.',
                        'duration': '10-15 minutes',
                        'category': 'social'
                    }
                ],
                'anger': [
                    {
                        'title': 'Count to 10 Slowly',
                        'description': 'Take deep breaths and count slowly from 1 to 10 before responding.',
                        'duration': '1-2 minutes',
                        'category': 'mental'
                    },
                    {
                        'title': 'Physical Release',
                        'description': 'Do jumping jacks, push-ups, or squeeze a stress ball to release tension.',
                        'duration': '2-5 minutes',
                        'category': 'physical'
                    },
                    {
                        'title': 'Write It Down',
                        'description': 'Write about what made you angry without censoring yourself.',
                        'duration': '5-10 minutes',
                        'category': 'mental'
                    }
                ]
            },
            'hi': {
                'anxiety': [
                    {
                        'title': '5-4-3-2-1 ग्राउंडिंग तकनीक',
                        'description': '5 चीजें जो आप देख सकते हैं, 4 जो छू सकते हैं, 3 जो सुन सकते हैं, 2 जो सूंघ सकते हैं, 1 जो चख सकते हैं, उनके नाम बताएं।',
                        'duration': '2-3 मिनट',
                        'category': 'grounding'
                    },
                    {
                        'title': 'प्रगतिशील मांसपेशी शिथिलता',
                        'description': 'अपने पैर की उंगलियों से सिर तक प्रत्येक मांसपेशी समूह को तान कर फिर ढीला छोड़ें।',
                        'duration': '10-15 मिनट',
                        'category': 'relaxation'
                    },
                    {
                        'title': 'चेहरे पर ठंडा पानी',
                        'description': 'अपने चेहरे पर ठंडा पानी छिड़कें या बर्फ के टुकड़े पकड़ें।',
                        'duration': '1-2 मिनट',
                        'category': 'physical'
                    }
                ],
                'stress': [
                    {
                        'title': 'बॉक्स ब्रीदिंग',
                        'description': '4 गिनती में सांस लें, 4 में रोकें, 4 में छोड़ें, 4 में रोकें। दोहराएं।',
                        'duration': '5-10 मिनट',
                        'category': 'breathing'
                    },
                    {
                        'title': 'तेज चलना',
                        'description': '5 मिनट तेज चलें, अपने आस-पास और सांस पर ध्यान दें।',
                        'duration': '5 मिनट',
                        'category': 'physical'
                    },
                    {
                        'title': 'सकारात्मक पुष्टि',
                        'description': 'दोहराएं: "मैं सक्षम हूं, मैं मजबूत हूं, मैं इस स्थिति को संभाल सकता हूं।"',
                        'duration': '2-3 मिनट',
                        'category': 'mental'
                    }
                ],
                'sadness': [
                    {
                        'title': 'कृतज्ञता सूची',
                        'description': 'आज आप जिन 3 बातों के लिए आभारी हैं, उन्हें लिखें, चाहे वे कितनी भी छोटी हों।',
                        'duration': '5 मिनट',
                        'category': 'mental'
                    },
                    {
                        'title': 'हल्का व्यायाम',
                        'description': 'कुछ हल्की स्ट्रेचिंग या योग आसन करें।',
                        'duration': '10 मिनट',
                        'category': 'physical'
                    },
                    {
                        'title': 'किसी से जुड़ें',
                        'description': 'किसी मित्र, परिवारजन या सहायक व्यक्ति को फोन करें या संदेश भेजें।',
                        'duration': '10-15 मिनट',
                        'category': 'social'
                    }
                ],
                'anger': [
                    {
                        'title': '10 तक धीरे-धीरे गिनती करें',
                        'description': 'जवाब देने से पहले गहरी सांस लें और 1 से 10 तक धीरे-धीरे गिनें।',
                        'duration': '1-2 मिनट',
                        'category': 'mental'
                    },
                    {
                        'title': 'शारीरिक निकास',
                        'description': 'जंपिंग जैक्स, पुश-अप्स करें या स्ट्रेस बॉल दबाएं।',
                        'duration': '2-5 मिनट',
                        'category': 'physical'
                    },
                    {
                        'title': 'इसे लिख दें',
                        'description': 'जो बात आपको गुस्सा दिलाई है, उसके बारे में बिना रोक-टोक के लिखें।',
                        'duration': '5-10 मिनट',
                        'category': 'mental'
                    }
                ]
            }
        }
    
    def display_remedies_interface(self, language: str, emotion_level: int):
        """
        Display quick remedies interface.
        
        Args:
            language: Current language ('en' or 'hi')
            emotion_level: Current emotion level (1-10)
        """
        st.header(get_text("quick_remedies", language))
        st.markdown(get_text("remedies_description", language))
        
        # Emotion-based remedy suggestions
        emotion_category = self._get_emotion_category(emotion_level)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display suggested remedies based on emotion
            st.subheader(get_text("suggested_for_you", language))
            
            suggested_remedies = self.remedies[language].get(emotion_category, [])
            if suggested_remedies:
                for i, remedy in enumerate(suggested_remedies[:2]):  # Show top 2 suggestions
                    self._display_remedy_card(remedy, language, f"suggested_{i}")
            
            # All categories section
            st.subheader(get_text("all_remedies", language))
            
            # Category selection
            categories = list(self.remedies[language].keys())
            category_names = {
                'en': {
                    'anxiety': 'Anxiety & Panic',
                    'stress': 'Stress & Tension',
                    'sadness': 'Sadness & Low Mood',
                    'anger': 'Anger & Frustration'
                },
                'hi': {
                    'anxiety': 'चिंता और घबराहट',
                    'stress': 'तनाव और दबाव',
                    'sadness': 'उदासी और कम मूड',
                    'anger': 'गुस्सा और निराशा'
                }
            }
            
            selected_category = st.selectbox(
                get_text("select_category", language),
                categories,
                format_func=lambda x: category_names[language][x]
            )
            
            # Display remedies for selected category
            category_remedies = self.remedies[language][selected_category]
            for i, remedy in enumerate(category_remedies):
                self._display_remedy_card(remedy, language, f"{selected_category}_{i}")
        
        with col2:
            # Emergency resources
            self._display_emergency_resources(language)
            
            # Quick action buttons
            st.subheader(get_text("instant_help", language))
            
            if st.button(get_text("random_remedy", language)):
                random_remedy = self._get_random_remedy(language)
                st.info(f"**{random_remedy['title']}**\n\n{random_remedy['description']}")
            
            if st.button(get_text("breathing_reminder", language)):
                st.success(get_text("breathing_reminder_text", language))
            
            if st.button(get_text("positive_affirmation", language)):
                affirmation = self._get_random_affirmation(language)
                st.success(f"💫 {affirmation}")
            
            # Mood tracker integration
            st.subheader(get_text("current_state", language))
            st.write(f"{get_text('emotion_level', language)}: {emotion_level}/10")
            
            if emotion_level <= 4:
                st.warning(get_text("low_mood_message", language))
            elif emotion_level >= 8:
                st.success(get_text("good_mood_message", language))
            else:
                st.info(get_text("neutral_mood_message", language))
    
    def _display_remedy_card(self, remedy: Dict, language: str, key_suffix: str):
        """Display a remedy card with expand/collapse functionality."""
        with st.expander(f"💡 {remedy['title']} ({remedy['duration']})"):
            st.write(remedy['description'])
            
            # Category badge
            category_colors = {
                'breathing': '#4CAF50',
                'physical': '#2196F3', 
                'mental': '#FF9800',
                'grounding': '#9C27B0',
                'relaxation': '#00BCD4',
                'social': '#E91E63'
            }
            
            category_color = category_colors.get(remedy['category'], '#757575')
            st.markdown(
                f"""
                <div style="
                    background-color: {category_color};
                    color: white;
                    padding: 4px 8px;
                    border-radius: 12px;
                    display: inline-block;
                    font-size: 12px;
                    margin-top: 8px;
                ">
                    {remedy['category'].title()}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button(get_text("try_now", language), key=f"try_{key_suffix}"):
                    st.success(get_text("remedy_started", language))
            
            with col2:
                if st.button(get_text("set_reminder", language), key=f"remind_{key_suffix}"):
                    st.info(get_text("reminder_set", language))
    
    def _display_emergency_resources(self, language: str):
        """Display emergency mental health resources."""
        st.subheader(get_text("emergency_help", language))
        
        if language == 'hi':
            emergency_info = """
            **तत्काल सहायता चाहिए?**
            
            🆘 **संकटकालीन हेल्पलाइन:**
            - राष्ट्रीय मानसिक स्वास्थ्य: 1800-899-0019
            - KIRAN हेल्पलाइन: 1800-599-0019
            - Vandrevala हेल्पलाइन: 9999 666 555
            
            🏥 **तुरंत चिकित्सा सहायता लें यदि:**
            - आत्महत्या के विचार आ रहे हैं
            - खुद को या दूसरों को नुकसान पहुंचाने के विचार हैं
            - गंभीर पैनिक अटैक हो रहा है
            """
        else:
            emergency_info = """
            **Need immediate help?**
            
            🆘 **Crisis Helplines:**
            - National Suicide Prevention: 988
            - Crisis Text Line: Text HOME to 741741
            - NAMI Helpline: 1-800-950-NAMI
            
            🏥 **Seek immediate medical help if:**
            - Having thoughts of suicide
            - Thoughts of hurting yourself or others
            - Experiencing severe panic attacks
            """
        
        st.warning(emergency_info)
    
    def _get_emotion_category(self, emotion_level: int) -> str:
        """Determine emotion category based on level."""
        if emotion_level <= 3:
            return 'sadness'
        elif emotion_level <= 4:
            return 'stress'
        elif emotion_level <= 6:
            return 'anxiety'
        else:
            return random.choice(['stress', 'anxiety'])  # For higher emotions, general techniques
    
    def _get_random_remedy(self, language: str) -> Dict:
        """Get a random remedy from all categories."""
        all_remedies = []
        for category_remedies in self.remedies[language].values():
            all_remedies.extend(category_remedies)
        return random.choice(all_remedies)
    
    def _get_random_affirmation(self, language: str) -> str:
        """Get a random positive affirmation."""
        if language == 'hi':
            affirmations = [
                "मैं मजबूत हूं और मैं इस कठिन समय से गुजर जाऊंगा।",
                "मेरी भावनाएं अस्थायी हैं और बदल जाएंगी।",
                "मैं अपनी देखभाल करने का हकदार हूं।",
                "मैं हर दिन बेहतर हो रहा हूं।",
                "मेरे पास इस स्थिति से निपटने की शक्ति है।",
                "मैं अकेला नहीं हूं, मदद उपलब्ध है।",
                "मैं अपनी गति से ठीक हो रहा हूं।"
            ]
        else:
            affirmations = [
                "I am strong and I will get through this difficult time.",
                "My feelings are temporary and will change.",
                "I deserve to take care of myself.",
                "I am getting better every day.",
                "I have the strength to handle this situation.", 
                "I am not alone, help is available.",
                "I am healing at my own pace."
            ]
        
        return random.choice(affirmations)

    def get_situation_specific_remedies(self, situation: str, language: str) -> List[Dict]:
        """
        Get remedies for specific situations.
        
        Args:
            situation: Specific situation ('work_stress', 'relationship', 'health_anxiety', etc.)
            language: Current language
            
        Returns:
            List of relevant remedies
        """
        situation_mapping = {
            'work_stress': 'stress',
            'relationship': 'sadness', 
            'health_anxiety': 'anxiety',
            'financial_worry': 'stress',
            'family_issues': 'anger',
            'social_anxiety': 'anxiety'
        }
        
        category = situation_mapping.get(situation, 'stress')
        return self.remedies[language].get(category, [])
