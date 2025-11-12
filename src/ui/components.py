"""
Modern Streamlit UI components and utilities.
"""

import streamlit as st
import time
from typing import Optional, Dict, Any, List
from pathlib import Path
import base64

from src.utils.logger import get_logger

logger = get_logger(__name__)

class UIComponents:
    """Collection of modern UI components for Streamlit."""
    
    @staticmethod
    def setup_page_config(
        title: str = "PDF Converter Pro",
        icon: str = "📄",
        layout: str = "wide"
    ) -> None:
        """Set up page configuration with modern styling."""
        st.set_page_config(
            page_title=title,
            page_icon=icon,
            layout=layout,
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for modern look
        st.markdown("""
        <style>
        /* Main container styling */
        .main > div {
            padding-top: 2rem;
        }
        
        /* Custom button styling */
        .stButton > button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        }
        
        /* File uploader styling */
        .stFileUploader > div > div {
            border: 2px dashed #667eea;
            border-radius: 10px;
            padding: 2rem;
            background-color: #f8f9ff;
        }
        
        /* Success/Error message styling */
        .stSuccess {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 10px;
            padding: 1rem;
        }
        
        .stError {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 10px;
            padding: 1rem;
        }
        
        /* Card-like containers */
        .stContainer {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        
        /* Header styling */
        .main-header {
            text-align: center;
            color: #2c3e50;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .sub-header {
            text-align: center;
            color: #7f8c8d;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_header(title: str, subtitle: str = "") -> None:
        """Display modern header with gradient text."""
        st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)
        if subtitle:
            st.markdown(f'<p class="sub-header">{subtitle}</p>', unsafe_allow_html=True)
    
    @staticmethod
    def display_pdf_preview(pdf_file, height: int = 600) -> None:
        """Display PDF preview with modern styling."""
        try:
            # Reset file pointer
            pdf_file.seek(0)
            base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
            
            # Create styled PDF viewer
            pdf_display = f'''
            <div style="border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <iframe 
                    src="data:application/pdf;base64,{base64_pdf}" 
                    width="100%" 
                    height="{height}" 
                    type="application/pdf"
                    style="border: none;">
                </iframe>
            </div>
            '''
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            # Reset file pointer again
            pdf_file.seek(0)
            
        except Exception as e:
            logger.error(f"Failed to display PDF preview: {str(e)}")
            st.error("Could not display PDF preview")
    
    @staticmethod
    def display_progress_bar(
        progress: float, 
        message: str = "Processing...",
        show_percentage: bool = True
    ) -> None:
        """Display modern progress bar with message."""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.progress(progress)
        
        with col2:
            if show_percentage:
                st.write(f"{int(progress * 100)}%")
        
        st.write(f"**{message}**")
    
    @staticmethod
    def display_metrics(metrics: Dict[str, Any]) -> None:
        """Display metrics in a modern card layout."""
        cols = st.columns(len(metrics))
        
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i]:
                st.metric(
                    label=key,
                    value=value,
                    delta=None
                )
    
    @staticmethod
    def display_file_info(file_info: Dict[str, Any]) -> None:
        """Display file information in a structured format."""
        st.subheader("📋 File Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Filename:** {file_info.get('file_name', 'Unknown')}")
            st.write(f"**File Size:** {file_info.get('file_size_mb', 0):.2f} MB")
            st.write(f"**Pages:** {file_info.get('page_count', 0)}")
        
        with col2:
            st.write(f"**Title:** {file_info.get('title', 'N/A')}")
            st.write(f"**Author:** {file_info.get('author', 'N/A')}")
            st.write(f"**Creator:** {file_info.get('creator', 'N/A')}")
    
    @staticmethod
    def display_success_message(message: str, details: Optional[str] = None) -> None:
        """Display success message with modern styling."""
        st.success(f"✅ {message}")
        if details:
            with st.expander("View Details"):
                st.write(details)
    
    @staticmethod
    def display_error_message(message: str, details: Optional[str] = None) -> None:
        """Display error message with modern styling."""
        st.error(f"❌ {message}")
        if details:
            with st.expander("Error Details"):
                st.code(details)
    
    @staticmethod
    def display_info_message(message: str, icon: str = "ℹ️") -> None:
        """Display info message with modern styling."""
        st.info(f"{icon} {message}")
    
    @staticmethod
    def display_warning_message(message: str) -> None:
        """Display warning message with modern styling."""
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def create_download_button(
        data: bytes,
        filename: str,
        mime_type: str,
        label: str = "Download File"
    ) -> bool:
        """Create a styled download button."""
        return st.download_button(
            label=f"📥 {label}",
            data=data,
            file_name=filename,
            mime=mime_type,
            help=f"Click to download {filename}"
        )
    
    @staticmethod
    def display_processing_status(
        current_step: str,
        total_steps: int,
        current_step_num: int
    ) -> None:
        """Display processing status with step indicator."""
        # Progress calculation
        progress = current_step_num / total_steps
        
        # Display progress
        st.progress(progress)
        
        # Display current step
        st.write(f"**Step {current_step_num}/{total_steps}:** {current_step}")
        
        # Display step indicators
        step_cols = st.columns(total_steps)
        for i in range(total_steps):
            with step_cols[i]:
                if i < current_step_num:
                    st.write("✅")
                elif i == current_step_num - 1:
                    st.write("🔄")
                else:
                    st.write("⏳")
    
    @staticmethod
    def display_feature_cards(features: List[Dict[str, str]]) -> None:
        """Display feature cards in a grid layout."""
        cols = st.columns(len(features))
        
        for i, feature in enumerate(features):
            with cols[i]:
                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 1.5rem;
                    border-radius: 15px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    text-align: center;
                    height: 200px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                ">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">
                        {feature.get('icon', '📄')}
                    </div>
                    <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">
                        {feature.get('title', 'Feature')}
                    </h3>
                    <p style="color: #7f8c8d; font-size: 0.9rem;">
                        {feature.get('description', '')}
                    </p>
                </div>
                """, unsafe_allow_html=True)