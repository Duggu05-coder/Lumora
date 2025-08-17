# LumosAI - Mental Health Companion

## Overview

LumosAI is a comprehensive AI-powered mental health support application built with Streamlit featuring a stunning black, purple, and blue neon theme. The application provides multilingual therapy chat services, emotion tracking, breathing exercises, camera-based breathing analysis, and quick remedies. It integrates AI-powered therapy conversations using Google's Gemini API and includes real-time emotion monitoring capabilities. The system is designed to offer personalized mental health support with a modern, visually appealing neon interface that enhances the user experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application with multi-tab interface
- **UI Components**: Tabbed navigation system with dedicated sections for chat, emotion tracking, breathing exercises, camera analysis, remedies, and history
- **State Management**: Streamlit session state for maintaining user data across interactions
- **Responsive Design**: Wide layout configuration with sidebar for settings

### Backend Architecture
- **Modular Design**: Component-based architecture with separate classes for each major feature:
  - `TherapyBot`: AI-powered conversation management
  - `EmotionTracker`: Mood monitoring and visualization
  - `BreathingExercises`: Guided breathing sessions
  - `CameraAnalysis`: Computer vision for breathing detection
  - `QuickRemedies`: Instant coping strategies
  - `DataManager`: Data export and statistics

### AI Integration
- **Therapy Engine**: Google Gemini 2.5 Flash model for contextual therapy responses
- **Context Management**: Maintains conversation history for personalized interactions
- **Emotion-Aware Responses**: Adjusts therapy approach based on user's emotional state (1-10 scale)

### Multilingual Support
- **Translation System**: Comprehensive translation module supporting English and Hindi
- **Dynamic Language Switching**: Real-time language selection with interface updates
- **Localized Content**: All text, remedies, and breathing exercises available in both languages

### Data Visualization
- **Emotion Analytics**: Plotly charts for mood tracking over time
- **Progress Monitoring**: Statistical analysis of emotional patterns
- **Export Capabilities**: JSON and CSV export formats for user data

### Computer Vision
- **Breathing Detection**: OpenCV integration for camera-based breathing analysis
- **Real-time Processing**: Live video feed analysis for breathing patterns
- **Privacy-First**: Local processing without external data transmission

## External Dependencies

### Core Framework
- **Streamlit**: Web application framework for the entire user interface

### AI and Machine Learning
- **Google Gemini API**: Primary AI service for therapy conversations and responses
- **OpenCV**: Computer vision library for camera-based breathing analysis
- **NumPy**: Numerical computations for data processing

### Data Processing and Visualization
- **Pandas**: Data manipulation and analysis for user statistics
- **Plotly**: Interactive charting and visualization for emotion tracking

### Development Tools
- **JSON**: Data serialization for export functionality
- **Threading**: Concurrent processing for camera operations
- **DateTime**: Timestamp management for tracking and history

### Environment Configuration
- **Environment Variables**: Secure API key management for Gemini integration
- **Session Management**: Streamlit session state for user data persistence

The application follows a privacy-conscious approach with local data processing and optional cloud AI integration only for therapy conversations.