import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
import streamlit as st

class DataManager:
    def __init__(self):
        """Initialize data manager for handling user data storage and export."""
        pass
    
    def export_all_data(self, chat_history: List[Dict], emotion_history: List[Dict]) -> str:
        """
        Export all user data to JSON format.
        
        Args:
            chat_history: Chat conversation history
            emotion_history: Emotion tracking history
            
        Returns:
            JSON string with all data
        """
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'data_version': '1.0',
            'user_data': {
                'chat_history': chat_history,
                'emotion_history': emotion_history,
                'statistics': self._calculate_statistics(chat_history, emotion_history)
            }
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def export_chat_history_csv(self, chat_history: List[Dict]) -> str:
        """
        Export chat history to CSV format.
        
        Args:
            chat_history: Chat conversation history
            
        Returns:
            CSV string
        """
        if not chat_history:
            return "timestamp,role,content,emotion\n"
        
        df = pd.DataFrame(chat_history)
        return df.to_csv(index=False)
    
    def export_emotion_history_csv(self, emotion_history: List[Dict]) -> str:
        """
        Export emotion history to CSV format.
        
        Args:
            emotion_history: Emotion tracking history
            
        Returns:
            CSV string
        """
        if not emotion_history:
            return "timestamp,emotion\n"
        
        df = pd.DataFrame(emotion_history)
        return df.to_csv(index=False)
    
    def _calculate_statistics(self, chat_history: List[Dict], emotion_history: List[Dict]) -> Dict[str, Any]:
        """Calculate statistics from user data."""
        stats = {
            'total_chat_messages': len(chat_history),
            'total_emotion_entries': len(emotion_history),
            'user_messages': len([msg for msg in chat_history if msg.get('role') == 'user']),
            'bot_messages': len([msg for msg in chat_history if msg.get('role') == 'assistant'])
        }
        
        # Emotion statistics
        if emotion_history:
            emotions = [entry['emotion'] for entry in emotion_history]
            stats.update({
                'average_emotion': sum(emotions) / len(emotions),
                'highest_emotion': max(emotions),
                'lowest_emotion': min(emotions),
                'emotion_trend': self._calculate_emotion_trend(emotions)
            })
        
        # Time-based statistics
        if chat_history:
            timestamps = [msg.get('timestamp') for msg in chat_history if msg.get('timestamp')]
            if timestamps:
                stats.update({
                    'first_session': min(timestamps),
                    'last_session': max(timestamps),
                    'session_span_days': self._calculate_day_span(timestamps)
                })
        
        return stats
    
    def _calculate_emotion_trend(self, emotions: List[int]) -> str:
        """Calculate overall emotion trend."""
        if len(emotions) < 2:
            return 'insufficient_data'
        
        # Simple trend calculation using first and last thirds
        first_third = emotions[:len(emotions)//3] if len(emotions) >= 9 else emotions[:1]
        last_third = emotions[-len(emotions)//3:] if len(emotions) >= 9 else emotions[-1:]
        
        avg_first = sum(first_third) / len(first_third)
        avg_last = sum(last_third) / len(last_third)
        
        difference = avg_last - avg_first
        
        if difference > 0.5:
            return 'improving'
        elif difference < -0.5:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_day_span(self, timestamps: List[str]) -> int:
        """Calculate number of days between first and last session."""
        try:
            dates = [datetime.fromisoformat(ts.replace('Z', '+00:00')).date() 
                    for ts in timestamps if ts]
            if len(dates) >= 2:
                return (max(dates) - min(dates)).days
            return 0
        except Exception:
            return 0
    
    def import_data(self, json_data: str) -> Dict[str, Any]:
        """
        Import data from JSON string.
        
        Args:
            json_data: JSON string with user data
            
        Returns:
            Dictionary with imported data
        """
        try:
            data = json.loads(json_data)
            return data.get('user_data', {})
        except json.JSONDecodeError:
            return {}
    
    def validate_data_integrity(self, data: Dict) -> bool:
        """
        Validate data integrity.
        
        Args:
            data: Data dictionary to validate
            
        Returns:
            True if data is valid
        """
        required_fields = ['chat_history', 'emotion_history']
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate chat history structure
        if isinstance(data['chat_history'], list):
            for msg in data['chat_history']:
                if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
                    return False
        
        # Validate emotion history structure
        if isinstance(data['emotion_history'], list):
            for entry in data['emotion_history']:
                if not isinstance(entry, dict) or 'emotion' not in entry:
                    return False
                if not isinstance(entry['emotion'], (int, float)):
                    return False
                if entry['emotion'] < 1 or entry['emotion'] > 10:
                    return False
        
        return True
    
    def clear_user_data(self) -> bool:
        """
        Clear all user data from session state.
        
        Returns:
            True if successful
        """
        try:
            if 'chat_history' in st.session_state:
                st.session_state.chat_history = []
            if 'emotion_history' in st.session_state:
                st.session_state.emotion_history = []
            if 'current_emotion' in st.session_state:
                st.session_state.current_emotion = 5
            return True
        except Exception:
            return False
    
    def get_data_summary(self, chat_history: List[Dict], emotion_history: List[Dict]) -> Dict[str, Any]:
        """
        Get a summary of user data for display.
        
        Args:
            chat_history: Chat conversation history
            emotion_history: Emotion tracking history
            
        Returns:
            Summary dictionary
        """
        summary = {
            'total_conversations': len([msg for msg in chat_history if msg.get('role') == 'user']),
            'total_emotion_logs': len(emotion_history),
            'data_size_kb': len(json.dumps({'chat': chat_history, 'emotions': emotion_history})) / 1024
        }
        
        if emotion_history:
            emotions = [entry['emotion'] for entry in emotion_history]
            summary.update({
                'avg_emotion': round(sum(emotions) / len(emotions), 1),
                'emotion_range': f"{min(emotions)}-{max(emotions)}"
            })
        
        if chat_history:
            timestamps = [msg.get('timestamp') for msg in chat_history if msg.get('timestamp')]
            if timestamps:
                try:
                    first_date = min(timestamps)[:10]  # YYYY-MM-DD
                    last_date = max(timestamps)[:10]
                    summary.update({
                        'first_session': first_date,
                        'last_session': last_date
                    })
                except Exception:
                    pass
        
        return summary
