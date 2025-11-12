"""
Table extraction implementation for converting PDF tables to Excel.
"""

import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from pdf2image import convert_from_path
from img2table.ocr import PaddleOCR
from img2table.document import PDF

from src.core.interfaces import TableExtractor
from src.core.pdf_processor import PDFProcessorImpl
from src.utils.exceptions import PDFReadError, ConversionError, ValidationError
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TableExtractorImpl(TableExtractor):
    """Professional table extractor implementation."""
    
    def __init__(self, confidence_threshold: int = 50):
        """Initialize table extractor.
        
        Args:
            confidence_threshold: Minimum confidence threshold for table detection
        """
        self.confidence_threshold = confidence_threshold
        self.pdf_processor = PDFProcessorImpl()
        
        logger.info(f"Table extractor initialized with confidence threshold: {confidence_threshold}")
    
    def extract_tables(
        self, 
        file_path: Path, 
        pages: Optional[List[int]] = None,
        language: str = "eng"
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Extract tables from PDF and save as Excel.
        
        Args:
            file_path: Path to PDF file
            pages: List of page numbers to process (1-indexed), None for all pages
            language: Language code for OCR (en, fr, etc.)
            
        Returns:
            Tuple of (excel_file_path, extracted_tables_metadata)
            
        Raises:
            PDFReadError: If PDF cannot be read
            ConversionError: If table extraction fails
        """
        try:
            # Validate PDF file
            self.pdf_processor.validate_file(file_path)
            total_pages = self.pdf_processor.get_page_count(file_path)
            
            # Determine pages to process
            if pages is None:
                pages_to_process = list(range(1, total_pages + 1))
            else:
                # Validate page numbers
                invalid_pages = [p for p in pages if p < 1 or p > total_pages]
                if invalid_pages:
                    raise ValidationError(f"Invalid page numbers: {invalid_pages}")
                pages_to_process = sorted(pages)
            
            logger.info(f"Extracting tables from {len(pages_to_process)} pages in {language}")
            
            # Convert language code
            ocr_language = self._convert_language_code(language)
            
            # Initialize PaddleOCR
            paddle_ocr = PaddleOCR(
                lang=ocr_language, 
                kw={"use_dilation": True, "use_angle_cls": True}
            )
            
            # Initialize PDF document for table extraction
            # Convert 1-indexed pages to 0-indexed for img2table
            zero_indexed_pages = [p - 1 for p in pages_to_process] if pages_to_process else None
            
            doc = PDF(
                str(file_path), 
                pages=zero_indexed_pages,
                detect_rotation=True,
                pdf_text_extraction=True
            )
            
            # Extract tables
            logger.debug("Starting table extraction...")
            extracted_tables = doc.extract_tables(
                ocr=paddle_ocr,
                implicit_rows=True,
                borderless_tables=True,
                min_confidence=self.confidence_threshold
            )
            
            logger.info(f"Extracted {len(extracted_tables)} tables")
            
            # Create temporary Excel file
            with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp_file:
                excel_file_path = tmp_file.name
            
            # Save tables to Excel
            doc.to_xlsx(
                excel_file_path,
                ocr=paddle_ocr,
                implicit_rows=True,
                borderless_tables=True,
                min_confidence=self.confidence_threshold
            )
            
            # Generate metadata about extracted tables
            tables_metadata = self._generate_tables_metadata(extracted_tables, pages_to_process)
            
            logger.info(f"Tables saved to Excel file: {excel_file_path}")
            return excel_file_path, tables_metadata
            
        except Exception as e:
            logger.error(f"Table extraction failed for {file_path}: {str(e)}")
            if isinstance(e, (PDFReadError, ValidationError)):
                raise
            raise ConversionError(f"Table extraction failed: {str(e)}")
    
    def _convert_language_code(self, language: str) -> str:
        """Convert language code to PaddleOCR format.
        
        Args:
            language: Input language code (eng, fra, etc.)
            
        Returns:
            PaddleOCR language code
        """
        language_mapping = {
            'eng': 'en',
            'fra': 'fr',
            'deu': 'de',
            'spa': 'es',
            'ita': 'it',
            'por': 'pt',
            'rus': 'ru',
            'jpn': 'ja',
            'kor': 'ko',
            'chi_sim': 'ch',
            'chi_tra': 'ch'
        }
        
        return language_mapping.get(language, 'en')
    
    def _generate_tables_metadata(
        self, 
        extracted_tables: List[Any], 
        pages: List[int]
    ) -> List[Dict[str, Any]]:
        """Generate metadata about extracted tables.
        
        Args:
            extracted_tables: List of extracted table objects
            pages: List of processed page numbers
            
        Returns:
            List of metadata dictionaries
        """
        metadata = []
        
        for i, table in enumerate(extracted_tables):
            try:
                # Extract basic table information
                table_info = {
                    'table_id': i + 1,
                    'page_number': getattr(table, 'page', 'Unknown'),
                    'bbox': getattr(table, 'bbox', None),
                    'confidence': getattr(table, 'confidence', None),
                    'rows': len(table.content) if hasattr(table, 'content') else 0,
                    'columns': len(table.content[0]) if (hasattr(table, 'content') and table.content) else 0
                }
                
                metadata.append(table_info)
                
            except Exception as e:
                logger.warning(f"Failed to extract metadata for table {i + 1}: {str(e)}")
                metadata.append({
                    'table_id': i + 1,
                    'page_number': 'Unknown',
                    'error': str(e)
                })
        
        return metadata