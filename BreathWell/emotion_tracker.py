import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
from translations import get_text

class EmotionTracker:
    def __init__(self):
        """Initialize the emotion tracker."""
        self.emotion_labels = {
            'en': {
                1: "💔 Crisis/Trauma",
                2: "😠 Angry/Very Sad", 
                3: "😕 Down",
                4: "😐 Low",
                5: "😶 Neutral",
                6: "🙂 Okay",
                7: "😊 Good",
                8: "😄 Happy",
                9: "😁 Very Happy",
                10: "🤩 Excellent"
            },
            'hi': {
                1: "💔 गंभीर स्थिति/आघात",
                2: "😠 क्रोधित/बहुत दुखी",
                3: "😕 निराश",
                4: "😐 कम",
                5: "😶 सामान्य",
                6: "🙂 ठीक",
                7: "😊 अच्छा",
                8: "😄 खुश",
                9: "😁 बहुत खुश",
                10: "🤩 उत्कृष्ट"
            }
        }
    
    def display_emotion_interface(self, language: str) -> int:
        """
        Display emotion tracking interface.
        
        Args:
            language: Current language ('en' or 'hi')
            
        Returns:
            Selected emotion level (1-10)
        """
        st.header(get_text("emotion_tracking", language))
        st.markdown(get_text("emotion_description", language))
        
        # Current emotion meter
        col1, col2 = st.columns([2, 1])
        
        with col1:
            current_emotion = st.slider(
                get_text("current_emotion", language),
                min_value=1,
                max_value=10,
                value=st.session_state.get('current_emotion', 5),
                help=get_text("emotion_help", language)
            )
            
            # Display emotion label
            emotion_label = self.emotion_labels[language][current_emotion]
            st.markdown(f"### {emotion_label}")
            
        with col2:
            # Emotion color indicator
            color = self._get_emotion_color(current_emotion)
            st.markdown(
                f"""
                <div style="
                    background-color: {color};
                    width: 100px;
                    height: 100px;
                    border-radius: 50%;
                    margin: 20px auto;
                    border: 3px solid #fff;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                "></div>
                """,
                unsafe_allow_html=True
            )
            
            # Emotion level text
            st.markdown(f"**{current_emotion}/10**", unsafe_allow_html=True)
        
        # Log emotion button
        if st.button(get_text("log_emotion", language)):
            st.success(get_text("emotion_logged", language))
            return current_emotion
            
        # Quick emotion buttons
        st.subheader(get_text("quick_emotions", language))
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("😢 1"):
                return 1
        with col2:
            if st.button("😔 3"):
                return 3
        with col3:
            if st.button("😶 5"):
                return 5
        with col4:
            if st.button("😊 7"):
                return 7
        with col5:
            if st.button("🤩 10"):
                return 10
        
        return current_emotion
    
    def display_emotion_timeline(self, emotion_history: List[Dict], language: str):
        """
        Display emotion timeline chart.
        
        Args:
            emotion_history: List of emotion entries with timestamps
            language: Current language
        """
        if not emotion_history:
            st.info(get_text("no_emotion_data", language))
            return
            
        st.subheader(get_text("emotion_timeline", language))
        
        # Convert to DataFrame
        df = pd.DataFrame(emotion_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Time range selector
        time_range = st.selectbox(
            get_text("time_range", language),
            options=['1d', '7d', '30d', 'all'],
            format_func=lambda x: get_text(f"range_{x}", language)
        )
        
        # Filter data based on time range
        if time_range != 'all':
            days_map = {'1d': 1, '7d': 7, '30d': 30}
            cutoff_date = datetime.now() - timedelta(days=days_map[time_range])
            df_filtered = df[df['timestamp'] >= cutoff_date]
        else:
            df_filtered = df
            
        if df_filtered.empty:
            st.info(get_text("no_data_range", language))
            return
        
        # Create timeline chart
        fig = go.Figure()
        
        # Add emotion line
        fig.add_trace(go.Scatter(
            x=df_filtered['timestamp'],
            y=df_filtered['emotion'],
            mode='lines+markers',
            name=get_text("emotion_level", language),
            line=dict(color='#ff6b6b', width=3),
            marker=dict(
                size=8,
                color=df_filtered['emotion'].apply(self._get_emotion_color),
                line=dict(width=2, color='white')
            ),
            hovertemplate='<b>%{y}/10</b><br>%{x}<extra></extra>'
        ))
        
        # Add average line
        avg_emotion = df_filtered['emotion'].mean()
        fig.add_hline(
            y=avg_emotion,
            line_dash="dash",
            line_color="gray",
            annotation_text=f"{get_text('average', language)}: {avg_emotion:.1f}"
        )
        
        # Update layout
        fig.update_layout(
            title=get_text("emotion_over_time", language),
            xaxis_title=get_text("time", language),
            yaxis_title=get_text("emotion_level", language),
            yaxis=dict(range=[0, 11], tickmode='linear', tick0=1, dtick=1),
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Emotion statistics
        self._display_emotion_stats(df_filtered, language)
    
    def _display_emotion_stats(self, df: pd.DataFrame, language: str):
        """Display emotion statistics."""
        if df.empty:
            return
            
        st.subheader(get_text("emotion_stats", language))
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                get_text("average_emotion", language),
                f"{df['emotion'].mean():.1f}/10"
            )
            
        with col2:
            st.metric(
                get_text("highest_emotion", language),
                f"{df['emotion'].max()}/10"
            )
            
        with col3:
            st.metric(
                get_text("lowest_emotion", language),
                f"{df['emotion'].min()}/10"
            )
            
        with col4:
            st.metric(
                get_text("total_entries", language),
                len(df)
            )
        
        # Most frequent emotion
        most_common = df['emotion'].mode().iloc[0] if not df['emotion'].mode().empty else 5
        st.info(f"{get_text('most_common_emotion', language)}: {self.emotion_labels[language][most_common]}")
    
    def _get_emotion_color(self, emotion: int) -> str:
        """Get neon color for emotion level."""
        colors = {
            1: '#FF073A',  # Neon red
            2: '#FF2D92',  # Neon pink
            3: '#FF6B35',  # Neon orange
            4: '#FFB627',  # Neon yellow-orange
            5: '#FFEA00',  # Neon yellow
            6: '#ADFF2F',  # Neon green-yellow
            7: '#39FF14',  # Neon green
            8: '#00FFFF',  # Neon cyan
            9: '#1E90FF',  # Neon blue
            10: '#9D4EDD'  # Neon purple (brand color)
        }
        return colors.get(emotion, '#FFEA00')
