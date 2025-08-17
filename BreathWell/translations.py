"""
Translation module for multilingual support in the therapy chatbot.
Supports English (en) and Hindi (hi) languages.
"""

LANGUAGES = {
    'en': 'English',
    'hi': 'हिंदी (Hindi)'
}

TRANSLATIONS = {
    # Main interface
    'main_title': {
        'en': '✨ LumosAI - Mental Health Companion',
        'hi': '✨ LumosAI - मानसिक स्वास्थ्य साथी'
    },
    'welcome_message': {
        'en': 'Your AI-powered mental health companion with multilingual support, emotion tracking, breathing exercises, and camera analysis. Experience personalized therapy in English and Hindi.',
        'hi': 'आपका AI-संचालित मानसिक स्वास्थ्य साथी बहुभाषी समर्थन, भावना ट्रैकिंग, सांस अभ्यास और कैमरा विश्लेषण के साथ। अंग्रेजी और हिंदी में व्यक्तिगत चिकित्सा का अनुभव करें।'
    },
    
    # Navigation tabs
    'chat_tab': {
        'en': '💬 Chat',
        'hi': '💬 चैट'
    },
    'emotion_tab': {
        'en': '😊 Emotions',
        'hi': '😊 भावनाएं'
    },
    'breathing_tab': {
        'en': '🫁 Breathing',
        'hi': '🫁 सांस'
    },
    'camera_tab': {
        'en': '📹 Camera',
        'hi': '📹 कैमरा'
    },
    'remedies_tab': {
        'en': '💡 Remedies',
        'hi': '💡 उपचार'
    },
    'history_tab': {
        'en': '📊 History',
        'hi': '📊 इतिहास'
    },
    
    # Chat interface
    'therapy_chat': {
        'en': 'Therapy Chat Session',
        'hi': 'चिकित्सा चैट सत्र'
    },
    'chat_placeholder': {
        'en': 'How are you feeling today? Share what\'s on your mind...',
        'hi': 'आज आप कैसा महसूस कर रहे हैं? अपने मन की बात साझा करें...'
    },
    'thinking': {
        'en': 'Thinking...',
        'hi': 'सोच रहा हूं...'
    },
    'emotion': {
        'en': 'Emotion',
        'hi': 'भावना'
    },
    
    # Emotion tracking
    'emotion_tracking': {
        'en': 'Emotion Tracking',
        'hi': 'भावना ट्रैकिंग'
    },
    'emotion_description': {
        'en': 'Track your current emotional state to help personalize your therapy experience.',
        'hi': 'अपनी चिकित्सा अनुभव को व्यक्तिगत बनाने के लिए अपनी वर्तमान भावनात्मक स्थिति को ट्रैक करें।'
    },
    'current_emotion': {
        'en': 'How are you feeling right now?',
        'hi': 'आप अभी कैसा महसूस कर रहे हैं?'
    },
    'emotion_help': {
        'en': '1 = Very Sad, 5 = Neutral, 10 = Very Happy',
        'hi': '1 = बहुत उदास, 5 = तटस्थ, 10 = बहुत खुश'
    },
    'log_emotion': {
        'en': 'Log Current Emotion',
        'hi': 'वर्तमान भावना लॉग करें'
    },
    'emotion_logged': {
        'en': 'Emotion logged successfully!',
        'hi': 'भावना सफलतापूर्वक लॉग हो गई!'
    },
    'quick_emotions': {
        'en': 'Quick Emotion Selection',
        'hi': 'त्वरित भावना चयन'
    },
    'no_emotion_data': {
        'en': 'No emotion data available yet. Start logging your emotions!',
        'hi': 'अभी तक कोई भावना डेटा उपलब्ध नहीं है। अपनी भावनाओं को लॉग करना शुरू करें!'
    },
    'emotion_timeline': {
        'en': 'Emotion Timeline',
        'hi': 'भावना समयरेखा'
    },
    'time_range': {
        'en': 'Time Range',
        'hi': 'समय सीमा'
    },
    'range_1d': {
        'en': 'Last 24 Hours',
        'hi': 'पिछले 24 घंटे'
    },
    'range_7d': {
        'en': 'Last 7 Days',
        'hi': 'पिछले 7 दिन'
    },
    'range_30d': {
        'en': 'Last 30 Days',
        'hi': 'पिछले 30 दिन'
    },
    'range_all': {
        'en': 'All Time',
        'hi': 'सभी समय'
    },
    'no_data_range': {
        'en': 'No data available for selected time range.',
        'hi': 'चयनित समय सीमा के लिए कोई डेटा उपलब्ध नहीं है।'
    },
    'emotion_level': {
        'en': 'Emotion Level',
        'hi': 'भावना स्तर'
    },
    'time': {
        'en': 'Time',
        'hi': 'समय'
    },
    'average': {
        'en': 'Average',
        'hi': 'औसत'
    },
    'emotion_over_time': {
        'en': 'Emotion Over Time',
        'hi': 'समय के साथ भावना'
    },
    'emotion_stats': {
        'en': 'Emotion Statistics',
        'hi': 'भावना आंकड़े'
    },
    'average_emotion': {
        'en': 'Average Emotion',
        'hi': 'औसत भावना'
    },
    'highest_emotion': {
        'en': 'Highest Emotion',
        'hi': 'सर्वोच्च भावना'
    },
    'lowest_emotion': {
        'en': 'Lowest Emotion',
        'hi': 'सबसे कम भावना'
    },
    'total_entries': {
        'en': 'Total Entries',
        'hi': 'कुल प्रविष्टियां'
    },
    'most_common_emotion': {
        'en': 'Most Common Emotion',
        'hi': 'सबसे आम भावना'
    },
    
    # Breathing exercises
    'breathing_exercises': {
        'en': 'Guided Breathing Exercises',
        'hi': 'निर्देशित सांस अभ्यास'
    },
    'breathing_description': {
        'en': 'Practice breathing techniques to reduce stress and anxiety.',
        'hi': 'तनाव और चिंता कम करने के लिए सांस की तकनीकों का अभ्यास करें।'
    },
    'select_exercise': {
        'en': 'Select Breathing Exercise',
        'hi': 'सांस अभ्यास चुनें'
    },
    'description': {
        'en': 'Description',
        'hi': 'विवरण'
    },
    'benefits': {
        'en': 'Benefits',
        'hi': 'लाभ'
    },
    'settings': {
        'en': 'Settings',
        'hi': 'सेटिंग्स'
    },
    'number_of_rounds': {
        'en': 'Number of Rounds',
        'hi': 'राउंड की संख्या'
    },
    'start_exercise': {
        'en': 'Start Exercise',
        'hi': 'अभ्यास शुरू करें'
    },
    'visual_guide': {
        'en': 'Visual Guide',
        'hi': 'दृश्य गाइड'
    },
    'breathing_tips': {
        'en': 'Breathing Tips',
        'hi': 'सांस लेने की युक्तियां'
    },
    'exercise_in_progress': {
        'en': 'Exercise in Progress',
        'hi': 'अभ्यास चल रहा है'
    },
    'round': {
        'en': 'Round',
        'hi': 'राउंड'
    },
    'rest': {
        'en': 'Rest',
        'hi': 'आराम'
    },
    'exercise_completed': {
        'en': 'Exercise Completed!',
        'hi': 'अभ्यास पूरा हुआ!'
    },
    'well_done': {
        'en': 'Well done! How do you feel?',
        'hi': 'बहुत बढ़िया! आप कैसा महसूस कर रहे हैं?'
    },
    'exercise_error': {
        'en': 'Exercise Error',
        'hi': 'अभ्यास त्रुटि'
    },
    
    # Camera analysis
    'camera_analysis': {
        'en': 'Camera-Based Breathing Analysis',
        'hi': 'कैमरा-आधारित सांस विश्लेषण'
    },
    'camera_description': {
        'en': 'Use your camera to analyze breathing patterns and get personalized feedback.',
        'hi': 'सांस के पैटर्न का विश्लेषण करने और व्यक्तिगत फीडबैक प्राप्त करने के लिए अपने कैमरे का उपयोग करें।'
    },
    'camera_permission': {
        'en': '⚠️ Camera access required for breathing analysis',
        'hi': '⚠️ सांस विश्लेषण के लिए कैमरा एक्सेस आवश्यक है'
    },
    'camera_instructions': {
        'en': 'Please allow camera access in your browser settings to use this feature.',
        'hi': 'कृपया इस सुविधा का उपयोग करने के लिए अपने ब्राउज़र सेटिंग्स में कैमरा एक्सेस की अनुमति दें।'
    },
    'start_analysis': {
        'en': 'Start Analysis',
        'hi': 'विश्लेषण शुरू करें'
    },
    'stop_analysis': {
        'en': 'Stop Analysis',
        'hi': 'विश्लेषण रोकें'
    },
    'clear_data': {
        'en': 'Clear Data',
        'hi': 'डेटा साफ करें'
    },
    'data_cleared': {
        'en': 'Data cleared successfully!',
        'hi': 'डेटा सफलतापूर्वक साफ हो गया!'
    },
    'analysis_results': {
        'en': 'Analysis Results',
        'hi': 'विश्लेषण परिणाम'
    },
    'breathing_rate': {
        'en': 'Breathing Rate',
        'hi': 'सांस दर'
    },
    'breaths_per_minute': {
        'en': 'breaths/min',
        'hi': 'सांस/मिनट'
    },
    'pattern': {
        'en': 'Pattern',
        'hi': 'पैटर्न'
    },
    'recommendations': {
        'en': 'Recommendations',
        'hi': 'सुझाव'
    },
    'no_analysis_data': {
        'en': 'No analysis data available. Start recording to see results.',
        'hi': 'कोई विश्लेषण डेटा उपलब्ध नहीं है। परिणाम देखने के लिए रिकॉर्डिंग शुरू करें।'
    },
    'camera_error': {
        'en': 'Unable to access camera. Please check your camera permissions.',
        'hi': 'कैमरा तक पहुंच नहीं है। कृपया अपनी कैमरा अनुमतियों की जांच करें।'
    },
    'face_detection_warning': {
        'en': 'Face detection may not work optimally.',
        'hi': 'चेहरा पहचान बेहतर तरीके से काम नहीं कर सकता है।'
    },
    'analysis_error': {
        'en': 'Analysis error',
        'hi': 'विश्लेषण त्रुटि'
    },
    'breathing_chart': {
        'en': 'Breathing Pattern Chart',
        'hi': 'सांस पैटर्न चार्ट'
    },
    'insufficient_data': {
        'en': 'Insufficient data for visualization.',
        'hi': 'दृश्यीकरण के लिए अपर्याप्त डेटा।'
    },
    'breathing_signal': {
        'en': 'Breathing Signal',
        'hi': 'सांस सिग्नल'
    },
    'breathing_pattern_over_time': {
        'en': 'Breathing Pattern Over Time',
        'hi': 'समय के साथ सांस पैटर्न'
    },
    'time_seconds': {
        'en': 'Time (seconds)',
        'hi': 'समय (सेकंड)'
    },
    'breathing_intensity': {
        'en': 'Breathing Intensity',
        'hi': 'सांस की तीव्रता'
    },
    
    # Quick remedies
    'quick_remedies': {
        'en': 'Quick Remedies & Coping Strategies',
        'hi': 'त्वरित उपचार और मुकाबला रणनीतियां'
    },
    'remedies_description': {
        'en': 'Immediate techniques and strategies to help you feel better right now.',
        'hi': 'तुरंत बेहतर महसूस करने के लिए तत्काल तकनीकें और रणनीतियां।'
    },
    'suggested_for_you': {
        'en': 'Suggested for You',
        'hi': 'आपके लिए सुझावित'
    },
    'all_remedies': {
        'en': 'All Remedies',
        'hi': 'सभी उपचार'
    },
    'select_category': {
        'en': 'Select Category',
        'hi': 'श्रेणी चुनें'
    },
    'emergency_help': {
        'en': 'Emergency Help',
        'hi': 'आपातकालीन सहायता'
    },
    'instant_help': {
        'en': 'Instant Help',
        'hi': 'तत्काल सहायता'
    },
    'random_remedy': {
        'en': 'Random Remedy',
        'hi': 'यादृच्छिक उपचार'
    },
    'breathing_reminder': {
        'en': 'Breathing Reminder',
        'hi': 'सांस अनुस्मारक'
    },
    'breathing_reminder_text': {
        'en': '🫁 Take 3 deep breaths: In... Hold... Out... You\'re doing great!',
        'hi': '🫁 3 गहरी सांसें लें: अंदर... रोकें... बाहर... आप बहुत अच्छा कर रहे हैं!'
    },
    'positive_affirmation': {
        'en': 'Positive Affirmation',
        'hi': 'सकारात्मक पुष्टि'
    },
    'current_state': {
        'en': 'Current State',
        'hi': 'वर्तमान स्थिति'
    },
    'low_mood_message': {
        'en': 'I notice you\'re feeling low. Please consider the suggested remedies.',
        'hi': 'मैंने देखा है कि आप कम महसूस कर रहे हैं। कृपया सुझावित उपचारों पर विचार करें।'
    },
    'good_mood_message': {
        'en': 'Great to see you\'re feeling good! Keep up the positive energy.',
        'hi': 'यह देखकर अच्छा लगा कि आप अच्छा महसूस कर रहे हैं! सकारात्मक ऊर्जा बनाए रखें।'
    },
    'neutral_mood_message': {
        'en': 'You\'re in a neutral state. Consider some activities to boost your mood.',
        'hi': 'आप तटस्थ अवस्था में हैं। अपने मूड को बढ़ाने के लिए कुछ गतिविधियों पर विचार करें।'
    },
    'try_now': {
        'en': 'Try Now',
        'hi': 'अभी करें'
    },
    'set_reminder': {
        'en': 'Set Reminder',
        'hi': 'रिमाइंडर सेट करें'
    },
    'remedy_started': {
        'en': 'Great! Take your time with this remedy.',
        'hi': 'बहुत अच्छा! इस उपचार के साथ अपना समय लें।'
    },
    'reminder_set': {
        'en': 'Reminder set! We\'ll help you remember to practice this.',
        'hi': 'रिमाइंडर सेट हो गया! हम आपको इसका अभ्यास करने में मदद करेंगे।'
    },
    
    # History and data
    'session_history': {
        'en': 'Session History & Data',
        'hi': 'सत्र इतिहास और डेटा'
    },
    'show_emotions': {
        'en': 'Show Emotions',
        'hi': 'भावनाएं दिखाएं'
    },
    'message_limit': {
        'en': 'Message Limit',
        'hi': 'संदेश सीमा'
    },
    'message': {
        'en': 'Message',
        'hi': 'संदेश'
    },
    'no_history': {
        'en': 'No conversation history yet. Start chatting to see your history!',
        'hi': 'अभी तक कोई बातचीत इतिहास नहीं है। अपना इतिहास देखने के लिए चैट करना शुरू करें!'
    },
    
    # Sidebar
    'quick_stats': {
        'en': 'Quick Stats',
        'hi': 'त्वरित आंकड़े'
    },
    'total_sessions': {
        'en': 'Total Sessions',
        'hi': 'कुल सत्र'
    },
    'current_mood': {
        'en': 'Current Mood',
        'hi': 'वर्तमान मूड'
    },
    'export_data': {
        'en': 'Export Data',
        'hi': 'डेटा निर्यात करें'
    },
    'download_data': {
        'en': 'Download Data',
        'hi': 'डेटा डाउनलोड करें'
    }
}

def get_text(key: str, language: str) -> str:
    """
    Get translated text for a given key and language.
    
    Args:
        key: Translation key
        language: Language code ('en' or 'hi')
        
    Returns:
        Translated text or the key if translation not found
    """
    return TRANSLATIONS.get(key, {}).get(language, key)

def get_available_languages() -> dict:
    """Get available languages dictionary."""
    return LANGUAGES.copy()

def is_language_supported(language: str) -> bool:
    """Check if a language is supported."""
    return language in LANGUAGES
