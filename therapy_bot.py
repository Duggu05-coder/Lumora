import os
import json
import streamlit as st
from datetime import datetime
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
from typing import List, Dict
from translations import get_text

class TherapyBot:
    def __init__(self):
        """Initialize the therapy bot with Gemini API."""
        if GEMINI_AVAILABLE:
            self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            self.model = "gemini-2.5-flash"
        else:
            self.client = None
            self.model = None
        
        # Initialize session state for therapy context
        if 'therapy_session_context' not in st.session_state:
            st.session_state.therapy_session_context = {
                'session_count': 0,
                'main_concerns': [],
                'progress_notes': [],
                'preferred_techniques': [],
                'current_goals': [],
                'user_name': None,
                'session_start_time': None
            }
    
    def get_response(self, user_input: str, language: str, emotion_level: int, context_history: List[Dict] = None) -> str:
        """
        Generate a therapy response based on user input, language, and emotional state.
        
        Args:
            user_input: User's message
            language: 'en' for English, 'hi' for Hindi
            emotion_level: Current emotion level (1-10)
            context_history: Previous conversation messages for context
            
        Returns:
            Therapy bot response in the requested language
        """
        try:
            # Build context from history
            context = ""
            if context_history and len(context_history) > 0:
                context = "Previous conversation context:\n"
                for msg in context_history[-3:]:  # Last 3 messages for context
                    role = "User" if msg["role"] == "user" else "Assistant"
                    context += f"{role}: {msg['content']}\n"
                context += "\n"
            
            # Create system prompt based on language and emotion
            if language == 'hi':
                system_prompt = f"""
                आप एक मित्र की तरह हैं जो मानसिक स्वास्थ्य के बारे में जानता है। बिल्कुल सामान्य बातचीत की तरह बात करें, औपचारिक थेरेपिस्ट की तरह नहीं।
                
                उपयोगकर्ता का मूड: {emotion_level}/10 (1=बहुत परेशान, 10=बहुत अच्छा)
                
                बातचीत के लिए:
                - एक समझदार दोस्त की तरह प्राकृतिक रूप से बात करें
                - आसान, रोज़ाना की भाषा का उपयोग करें - कोई औपचारिक शब्दावली नहीं
                - उनकी भावनाओं को समझने के लिए सवाल पूछें
                - जब मूड कम हो तो बातचीत में ही प्राकृतिक रूप से किताब, गाना या मज़ाक सुझाएं
                - सलाह को बातचीत में प्राकृतिक रूप से शामिल करें जैसे दोस्त करते हैं
                - गर्मजोशी से, सच्चे और समझने योग्य हों
                - तकनीकें सुझाते समय दोस्ताना सलाह की तरह कहें:
                  * "कुछ धीमी, गहरी सांसें लेने की कोशिश करो - जब मैं परेशान होता हूं तो यह बहुत मदद करता है"
                  * "कभी-कभी जब मैं चिंतित होता हूं, तो मैं आसपास देखता हूं और 5 चीजें गिनता हूं जो देख सकता हूं..."
                  * "क्या तुमने थोड़ी देर टहलने की कोशिश की है? ताज़ी हवा मूड के लिए कमाल होती है"
                  * "कुछ अच्छी किताब पढ़ने से मूड बेहतर होता है - कोई सुझाव चाहिए?"
                  * "कुछ अच्छा गाना सुनकर देखो - संगीत में जादू होता है"
                  * "हंसना सबसे अच्छी दवा है - कुछ मज़ेदार सुनाऊं?"
                
                {context}
                """
            else:
                system_prompt = f"""
                You are a warm, empathetic mental health companion who talks like a caring friend. Your goal is to provide genuine emotional support through natural conversation.
                
                User's current mood: {emotion_level}/10 (1=feeling really down, 10=feeling great)
                
                Conversation approach:
                - Talk like a supportive friend who understands mental health
                - Use everyday language - avoid clinical or formal terminology
                - Show genuine interest in their feelings and experiences
                - Ask thoughtful follow-up questions to help them process emotions
                - Validate their feelings before offering suggestions
                - Share relatable experiences when appropriate
                - When mood is low, naturally weave in book recommendations, song suggestions, or jokes during conversation
                - Offer practical coping strategies as friendly suggestions like a caring friend would
                
                Helpful techniques to suggest naturally:
                - Breathing exercises: "I find taking slow, deep breaths really helps when I'm overwhelmed"
                - Grounding techniques: "When my mind is racing, I try the 5-4-3-2-1 technique - name 5 things you see, 4 you hear..."
                - Movement: "Sometimes a quick walk or even just stretching can shift my whole mood"
                - Self-compassion: "Be kind to yourself - you'd comfort a friend going through this, right?"
                - Book recommendations: "Have you tried reading something uplifting? I love recommending books that help"
                - Music therapy: "Music can be incredibly healing - maybe try listening to something soothing"
                - Humor therapy: "Sometimes a good laugh is exactly what we need. Want to hear something funny?"
                - Mindfulness: "Focusing on the present moment for just a few minutes can be surprisingly calming"
                
                Remember:
                - Respond with empathy first, advice second
                - Keep responses conversational (2-4 sentences usually)
                - Ask one thoughtful question to keep the conversation flowing
                - If they seem in crisis, gently suggest professional help
                - Keep responses conversational and supportive, not clinical or overly formal
                
                {context}
                """
            
            # Generate response using simpler API format
            if self.client and GEMINI_AVAILABLE:
                try:
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=f"{system_prompt}\n\nUser: {user_input}"
                    )
                    bot_response = response.text if response.text else self._get_fallback_response(language)
                    
                    # Integrate remedies directly into the conversation response
                    if emotion_level <= 4:  # Low mood, provide remedies
                        remedies = self._get_integrated_remedies_for_chat(emotion_level, language)
                        if remedies:
                            # Add remedies naturally to the conversation
                            bot_response += f"\n\n{remedies}"
                    
                    return bot_response
                except Exception as e:
                    print(f"Error getting therapy response: {e}")
                    return self._get_fallback_response(language)
            else:
                return self._get_fallback_response(language)
            
        except Exception as e:
            print(f"Error getting therapy response: {e}")
            return self._get_fallback_response(language)
    
    def _get_fallback_response(self, language: str) -> str:
        """Provide a fallback response when API fails."""
        if language == 'hi':
            return """मुझे खुशी है कि आपने अपनी बात साझा की है। कभी-कभी तकनीकी समस्याएं आ सकती हैं, 
            लेकिन आपकी भावनाएं महत्वपूर्ण हैं। कुछ गहरी सांसें लें और याद रखें कि आप अकेले नहीं हैं। 
            क्या आप अपनी समस्या के बारे में और बताना चाहेंगे?"""
        else:
            return """I'm glad you shared with me. Sometimes we may experience technical difficulties, 
            but your feelings matter. Take a few deep breaths and remember you're not alone. 
            Would you like to tell me more about what you're experiencing?"""
    
    def _get_integrated_remedies_for_chat(self, emotion_level: int, language: str) -> str:
        """Get personalized remedies integrated naturally into conversation based on emotion level."""
        import random
        
        if language == 'hi':
            if emotion_level <= 2:  # Very sad/anxious
                books = ["'The Alchemist' - Paulo Coelho", "'Man's Search for Meaning' - Viktor Frankl", "'The Power of Now' - Eckhart Tolle"]
                songs = ["'Breathe Me' - Sia", "'Fix You' - Coldplay", "'Weightless' - Marconi Union"]
                jokes = [
                    "डॉक्टर: आपको क्या परेशानी है?\nमरीज़: मुझे लगता है मैं एक मच्छर हूं।\nडॉक्टर: कब से?\nमरीज़: जब से मैंने buzz करना शुरू किया है!",
                    "टीचर: राम, बताओ कि पानी कैसे बनता है?\nराम: आसान है मैडम, H को दो और O को मिला दो!\nटीचर: H2O कैसे?\nराम: हाँ, Thank U मैडम!"
                ]
                return f"""यहाँ कुछ चीज़ें हैं जो मदद कर सकती हैं:

📚 एक अच्छी किताब पढ़कर देखें - {random.choice(books)} बहुत शांति देती है और नया नज़रिया मिलता है।

🎵 कुछ सुकूनदायक संगीत सुनें - '{random.choice(songs)}' सुनकर गहरी सांस लें। संगीत में जादू होता है।

😄 थोड़ी हंसी भी काम आएगी: {random.choice(jokes)}

बस याद रखिएगा, आप अकेले नहीं हैं। कभी-कभी छोटी-छोटी चीज़ें बड़ा बदलाव लाती हैं। 💙"""
                
            elif emotion_level <= 4:  # Moderate low mood
                books = ["'The Happiness Project' - Gretchen Rubin", "'Big Magic' - Elizabeth Gilbert", "'Atomic Habits' - James Clear"]
                songs = ["'Here Comes the Sun' - The Beatles", "'Good as Hell' - Lizzo", "'Happy' - Pharrell Williams"]
                jokes = [
                    "पत्नी: आप हमेशा मेरी बात क्यों नहीं सुनते?\nपति: मैं सुनता हूं, बस कभी-कभी मैं agreement mode में नहीं होता!",
                    "बॉस: आज आप देर से क्यों आए?\nकर्मचारी: सर, ट्रैफिक में फंस गया था।\nबॉस: तो जल्दी क्यों नहीं निकले?\nकर्मचारी: सर, इतनी जल्दी तो ट्रैफिक भी नहीं निकला!"
                ]
                return f"""कुछ अच्छी चीज़ें जो आपका मूड बेहतर कर सकती हैं:

📖 {random.choice(books)} जैसी कोई प्रेरणादायक किताब पढ़ें - रोज़ थोड़ा-थोड़ा पढ़ना काफी है।

🎶 '{random.choice(songs)}' जैसा खुशमिज़ाज गाना लगाएं और साथ में हम्म करें या थोड़ा डांस करें!

😊 हंसने के लिए: {random.choice(jokes)}

10 मिनट की छोटी सी सैर या कोई पसंदीदा स्नैक भी मूड अच्छा कर देता है। 🌟"""
        else:
            if emotion_level <= 2:  # Very sad/anxious
                books = ["'The Alchemist' by Paulo Coelho", "'Man's Search for Meaning' by Viktor Frankl", "'The Power of Now' by Eckhart Tolle"]
                songs = ["'Breathe Me' by Sia", "'Fix You' by Coldplay", "'Weightless' by Marconi Union"]
                jokes = [
                    "Why don't scientists trust atoms? Because they make up everything!",
                    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
                    "Why did the scarecrow win an award? He was outstanding in his field!"
                ]
                return f"""Here are some things that might help right now:

📚 Try reading {random.choice(books)} - it's a gentle, comforting book that offers new perspective during tough times.

🎵 Listen to '{random.choice(songs)}' and take some deep breaths. Music has incredible healing power.

😄 And here's something to make you smile: {random.choice(jokes)}

Remember, you're not alone in this. Sometimes the smallest things can make the biggest difference. Take it one moment at a time. 💙"""
                
            elif emotion_level <= 4:  # Moderate low mood
                books = ["'The Happiness Project' by Gretchen Rubin", "'Big Magic' by Elizabeth Gilbert", "'Atomic Habits' by James Clear"]
                songs = ["'Here Comes the Sun' by The Beatles", "'Good as Hell' by Lizzo", "'Happy' by Pharrell Williams"]
                jokes = [
                    "Why don't eggs tell jokes? They'd crack each other up!",
                    "What do you call a fake noodle? An impasta!",
                    "Why did the coffee file a police report? It got mugged!"
                ]
                return f"""I have some mood-lifting suggestions for you:

📖 Pick up {random.choice(books)} - it's perfect for daily doses of positivity and motivation.

🎶 Put on '{random.choice(songs)}' and dance it out or sing along! Music is such a powerful mood shifter.

😊 Quick laugh break: {random.choice(jokes)}

Also, try a 10-minute walk outside or treat yourself to something small that makes you happy. You deserve it! 🌟"""
        
        return ""  # No remedies needed for higher mood levels

    def get_emotional_support_response(self, emotion_level: int, language: str) -> str:
        """
        Generate an emotional support message based on current emotion level.
        
        Args:
            emotion_level: Current emotion level (1-10)
            language: 'en' for English, 'hi' for Hindi
            
        Returns:
            Supportive message based on emotion level
        """
        try:
            if language == 'hi':
                if emotion_level <= 3:
                    prompt = "उपयोगकर्ता बहुत दुखी है। उन्हें सांत्वना और आशा दें।"
                elif emotion_level <= 6:
                    prompt = "उपयोगकर्ता थोड़ा परेशान है। उन्हें प्रेरणा और सकारात्मकता दें।"
                else:
                    prompt = "उपयोगकर्ता अच्छी स्थिति में है। उनकी खुशी को बनाए रखने में मदद करें।"
                
                system_prompt = f"आप एक दयालु मानसिक स्वास्थ्य परामर्शदाता हैं। हिंदी में जवाब दें। {prompt}"
            else:
                if emotion_level <= 3:
                    prompt = "The user is feeling very sad. Provide comfort and hope."
                elif emotion_level <= 6:
                    prompt = "The user is feeling somewhat troubled. Provide encouragement and positivity."
                else:
                    prompt = "The user is in a good state. Help maintain their happiness."
                
                system_prompt = f"You are a compassionate mental health counselor. Respond in English. {prompt}"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=system_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=300
                )
            )
            
            return response.text if response.text else self._get_fallback_response(language)
            
        except Exception as e:
            print(f"Error getting emotional support response: {e}")
            return self._get_fallback_response(language)
