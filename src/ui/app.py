"""
Modern PDF Converter Application with Professional UI.
"""

import streamlit as st
import tempfile
import io
from pathlib import Path
from typing import Optional, List, Dict, Any

from src.ui.components import UIComponents
from src.core.pdf_processor import PDFProcessorImpl, TextExtractorImpl
from src.core.table_extractor import TableExtractorImpl
from src.core.file_validator import FileValidatorImpl
from src.utils.config import config_manager
from src.utils.exceptions import PDFProcessingError
from src.utils.logger import setup_logger, get_logger

# Initialize logger
logger = get_logger(__name__)

class PDFConverterApp:
    """Modern PDF Converter Application."""
    
    def __init__(self):
        """Initialize the application."""
        self.config = config_manager.load_config()
        
        # Initialize components
        self.pdf_processor = PDFProcessorImpl(self.config.ocr.tesseract_path)
        self.text_extractor = TextExtractorImpl(
            self.config.ocr.tesseract_path,
            self.config.ocr.confidence_threshold
        )
        self.table_extractor = TableExtractorImpl(self.config.ocr.confidence_threshold)
        self.file_validator = FileValidatorImpl()
        
        logger.info("PDF Converter App initialized")
    
    def run(self):
        """Run the Streamlit application."""
        try:
            self._setup_ui()
            self._render_main_interface()
        except Exception as e:
            logger.error(f"Application error: {str(e)}")
            UIComponents.display_error_message(
                "Application Error",
                f"An unexpected error occurred: {str(e)}"
            )
    
    def _setup_ui(self):
        """Set up the user interface."""
        UIComponents.setup_page_config(
            title=self.config.ui.page_title,
            icon="📄",
            layout="wide"
        )
        
        # Display header
        UIComponents.display_header(
            "PDF Converter Pro",
            "Professional PDF to Text and Excel conversion with advanced OCR"
        )
        
        # Display features
        features = [
            {
                "icon": "📝",
                "title": "Text Extraction",
                "description": "Extract text from PDFs with high accuracy OCR"
            },
            {
                "icon": "📊",
                "title": "Table Conversion",
                "description": "Convert PDF tables to Excel format"
            },
            {
                "icon": "🌍",
                "title": "Multi-Language",
                "description": "Support for multiple languages including English and French"
            },
            {
                "icon": "⚡",
                "title": "Fast Processing",
                "description": "Optimized processing with progress tracking"
            }
        ]
        
        UIComponents.display_feature_cards(features)
        
        st.markdown("---")
    
    def _render_main_interface(self):
        """Render the main application interface."""
        # Sidebar configuration
        self._render_sidebar()
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self._render_upload_section()
        
        with col2:
            self._render_options_section()
        
        # Process uploaded file
        if st.session_state.get('uploaded_file') is not None:
            self._process_uploaded_file()
    
    def _render_sidebar(self):
        """Render sidebar with configuration options."""
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # Language selection
            language = st.selectbox(
                "OCR Language",
                options=self.config.ocr.supported_languages,
                index=0 if self.config.ocr.default_language == "eng" else 1,
                help="Select the primary language for OCR processing"
            )
            st.session_state['language'] = language
            
            # Confidence threshold
            confidence = st.slider(
                "OCR Confidence Threshold",
                min_value=0,
                max_value=100,
                value=self.config.ocr.confidence_threshold,
                help="Minimum confidence level for OCR text recognition"
            )
            st.session_state['confidence'] = confidence
            
            # Processing options
            st.subheader("Processing Options")
            
            show_preview = st.checkbox(
                "Show PDF Preview",
                value=self.config.ui.show_preview,
                help="Display PDF preview before processing"
            )
            st.session_state['show_preview'] = show_preview
            
            # About section
            st.markdown("---")
            st.subheader("About")
            st.markdown("""
            **PDF Converter Pro** is a professional tool for converting PDF documents 
            to text and Excel formats using advanced OCR technology.
            
            Built with:
            - Streamlit for the UI
            - PyTesseract for OCR
            - img2table for table extraction
            - PaddleOCR for enhanced recognition
            """)
    
    def _render_upload_section(self):
        """Render file upload section."""
        st.subheader("📄 Upload PDF File")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help=f"Maximum file size: {self.config.processing.max_file_size_mb} MB"
        )
        
        if uploaded_file is not None:
            try:
                # Validate file
                file_io = io.BytesIO(uploaded_file.read())
                uploaded_file.seek(0)  # Reset for later use
                
                self.file_validator.validate_file_type(file_io)
                self.file_validator.validate_file_size(
                    file_io, 
                    self.config.processing.max_file_size_mb
                )
                self.file_validator.validate_filename(uploaded_file.name)
                
                st.session_state['uploaded_file'] = uploaded_file
                UIComponents.display_success_message(
                    f"File '{uploaded_file.name}' uploaded successfully!"
                )
                
            except PDFProcessingError as e:
                UIComponents.display_error_message(str(e))
                return
    
    def _render_options_section(self):
        """Render processing options section."""
        if st.session_state.get('uploaded_file') is None:
            st.info("Upload a PDF file to see processing options")
            return
        
        st.subheader("🔧 Processing Options")
        
        # Conversion type
        conversion_type = st.radio(
            "Conversion Type",
            options=["Text Extraction", "Table to Excel"],
            help="Choose the type of conversion to perform"
        )
        st.session_state['conversion_type'] = conversion_type
        
        # Page selection
        if st.session_state.get('file_info'):
            total_pages = st.session_state['file_info']['page_count']
            
            page_option = st.radio(
                "Pages to Process",
                options=["All Pages", "Specific Pages"]
            )
            
            if page_option == "Specific Pages":
                selected_pages = st.multiselect(
                    "Select Pages",
                    options=list(range(1, total_pages + 1)),
                    help="Select specific pages to process"
                )
                st.session_state['selected_pages'] = selected_pages
            else:
                st.session_state['selected_pages'] = None
        
        # Process button
        if st.button("🚀 Start Processing", use_container_width=True):
            st.session_state['start_processing'] = True
    
    def _process_uploaded_file(self):
        """Process the uploaded PDF file."""
        uploaded_file = st.session_state['uploaded_file']
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = Path(tmp_file.name)
        
        try:
            # Extract file information
            if 'file_info' not in st.session_state:
                with st.spinner("Analyzing PDF file..."):
                    metadata = self.pdf_processor.extract_metadata(temp_path)
                    metadata['file_size_mb'] = metadata['file_size'] / (1024 * 1024)
                    st.session_state['file_info'] = metadata
            
            # Display file information
            UIComponents.display_file_info(st.session_state['file_info'])
            
            # Show PDF preview if enabled
            if st.session_state.get('show_preview', True):
                with st.expander("📖 PDF Preview", expanded=False):
                    uploaded_file.seek(0)
                    UIComponents.display_pdf_preview(uploaded_file)
            
            # Start processing if requested
            if st.session_state.get('start_processing', False):
                self._perform_conversion(temp_path)
                st.session_state['start_processing'] = False
        
        finally:
            # Clean up temporary file
            if temp_path.exists():
                temp_path.unlink()
    
    def _perform_conversion(self, pdf_path: Path):
        """Perform the actual PDF conversion."""
        conversion_type = st.session_state.get('conversion_type', 'Text Extraction')
        language = st.session_state.get('language', 'eng')
        selected_pages = st.session_state.get('selected_pages')
        
        try:
            if conversion_type == "Text Extraction":
                self._perform_text_extraction(pdf_path, language, selected_pages)
            else:
                self._perform_table_extraction(pdf_path, language, selected_pages)
                
        except PDFProcessingError as e:
            UIComponents.display_error_message(
                "Processing Failed",
                str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error during conversion: {str(e)}")
            UIComponents.display_error_message(
                "Unexpected Error",
                f"An unexpected error occurred: {str(e)}"
            )
    
    def _perform_text_extraction(
        self, 
        pdf_path: Path, 
        language: str, 
        selected_pages: Optional[List[int]]
    ):
        """Perform text extraction with progress tracking."""
        progress_container = st.container()
        
        with progress_container:
            # Step 1: Initialize
            UIComponents.display_processing_status("Initializing...", 3, 1)
            
            # Step 2: Extract text
            UIComponents.display_processing_status("Extracting text...", 3, 2)
            
            extracted_texts = self.text_extractor.extract_text(
                pdf_path, 
                pages=selected_pages,
                language=language
            )
            
            # Step 3: Complete
            UIComponents.display_processing_status("Processing complete!", 3, 3)
        
        # Display results
        st.success("✅ Text extraction completed successfully!")
        
        # Show extracted text
        with st.expander("📝 Extracted Text", expanded=True):
            for i, text in enumerate(extracted_texts):
                page_num = selected_pages[i] if selected_pages else i + 1
                st.subheader(f"Page {page_num}")
                st.text_area(
                    f"Text from page {page_num}",
                    value=text,
                    height=200,
                    key=f"text_{page_num}"
                )
        
        # Download button
        all_text = "\n\n".join([
            f"=== Page {selected_pages[i] if selected_pages else i + 1} ===\n{text}"
            for i, text in enumerate(extracted_texts)
        ])
        
        UIComponents.create_download_button(
            data=all_text.encode('utf-8'),
            filename="extracted_text.txt",
            mime_type="text/plain",
            label="Download Text File"
        )
    
    def _perform_table_extraction(
        self, 
        pdf_path: Path, 
        language: str, 
        selected_pages: Optional[List[int]]
    ):
        """Perform table extraction with progress tracking."""
        progress_container = st.container()
        
        with progress_container:
            # Step 1: Initialize
            UIComponents.display_processing_status("Initializing...", 3, 1)
            
            # Step 2: Extract tables
            UIComponents.display_processing_status("Extracting tables...", 3, 2)
            
            excel_path, tables_metadata = self.table_extractor.extract_tables(
                pdf_path,
                pages=selected_pages,
                language=language
            )
            
            # Step 3: Complete
            UIComponents.display_processing_status("Processing complete!", 3, 3)
        
        # Display results
        st.success(f"✅ Extracted {len(tables_metadata)} tables successfully!")
        
        # Show table metadata
        if tables_metadata:
            with st.expander("📊 Extracted Tables Information", expanded=True):
                for table_info in tables_metadata:
                    st.json(table_info)
        
        # Download button
        with open(excel_path, 'rb') as excel_file:
            UIComponents.create_download_button(
                data=excel_file.read(),
                filename="extracted_tables.xlsx",
                mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                label="Download Excel File"
            )


def main():
    """Main application entry point."""
    # Setup logging
    setup_logger(
        name="pdf_converter",
        level="INFO",
        console_output=True
    )
    
    # Run application
    app = PDFConverterApp()
    app.run()


if __name__ == "__main__":
    main()