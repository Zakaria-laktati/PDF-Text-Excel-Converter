"""
PDF processing implementation with professional error handling and logging.
"""

import io
from pathlib import Path
from typing import List, Dict, Any, Optional
import tempfile

import pdf2image
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image

from src.core.interfaces import PDFProcessor, TextExtractor
from src.utils.exceptions import PDFReadError, OCRError, ValidationError
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PDFProcessorImpl(PDFProcessor):
    """Professional PDF processor implementation."""
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """Initialize PDF processor.
        
        Args:
            tesseract_path: Path to tesseract executable (optional)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        logger.info("PDF processor initialized")
    
    def validate_file(self, file_path: Path) -> bool:
        """Validate PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            True if file is valid PDF
            
        Raises:
            PDFReadError: If file cannot be read or is corrupted
        """
        try:
            if not file_path.exists():
                raise PDFReadError(f"File does not exist: {file_path}")
            
            if not file_path.suffix.lower() == '.pdf':
                raise ValidationError(f"File is not a PDF: {file_path}")
            
            # Try to read the PDF
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                if len(reader.pages) == 0:
                    raise PDFReadError("PDF file contains no pages")
            
            logger.debug(f"PDF file validated: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"PDF validation failed for {file_path}: {str(e)}")
            if isinstance(e, (PDFReadError, ValidationError)):
                raise
            raise PDFReadError(f"Invalid PDF file: {str(e)}")
    
    def get_page_count(self, file_path: Path) -> int:
        """Get total number of pages in PDF.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Number of pages
            
        Raises:
            PDFReadError: If file cannot be read
        """
        try:
            self.validate_file(file_path)
            
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                page_count = len(reader.pages)
            
            logger.debug(f"PDF has {page_count} pages: {file_path}")
            return page_count
            
        except Exception as e:
            logger.error(f"Failed to get page count for {file_path}: {str(e)}")
            if isinstance(e, PDFReadError):
                raise
            raise PDFReadError(f"Cannot read PDF file: {str(e)}")
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract PDF metadata.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary containing metadata
            
        Raises:
            PDFReadError: If file cannot be read
        """
        try:
            self.validate_file(file_path)
            
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                metadata = {
                    'page_count': len(reader.pages),
                    'file_size': file_path.stat().st_size,
                    'file_name': file_path.name
                }
                
                # Extract PDF metadata if available
                if reader.metadata:
                    pdf_metadata = reader.metadata
                    metadata.update({
                        'title': pdf_metadata.get('/Title', ''),
                        'author': pdf_metadata.get('/Author', ''),
                        'subject': pdf_metadata.get('/Subject', ''),
                        'creator': pdf_metadata.get('/Creator', ''),
                        'producer': pdf_metadata.get('/Producer', ''),
                        'creation_date': str(pdf_metadata.get('/CreationDate', '')),
                        'modification_date': str(pdf_metadata.get('/ModDate', ''))
                    })
            
            logger.debug(f"Extracted metadata for {file_path}: {metadata}")
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to extract metadata for {file_path}: {str(e)}")
            if isinstance(e, PDFReadError):
                raise
            raise PDFReadError(f"Cannot extract metadata: {str(e)}")

class TextExtractorImpl(TextExtractor):
    """Professional text extractor implementation using OCR."""
    
    def __init__(self, tesseract_path: Optional[str] = None, confidence_threshold: int = 50):
        """Initialize text extractor.
        
        Args:
            tesseract_path: Path to tesseract executable (optional)
            confidence_threshold: Minimum confidence threshold for OCR
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        self.confidence_threshold = confidence_threshold
        self.pdf_processor = PDFProcessorImpl(tesseract_path)
        
        logger.info(f"Text extractor initialized with confidence threshold: {confidence_threshold}")
    
    def extract_text(
        self, 
        file_path: Path, 
        pages: Optional[List[int]] = None,
        language: str = "eng"
    ) -> List[str]:
        """Extract text from PDF pages using OCR.
        
        Args:
            file_path: Path to PDF file
            pages: List of page numbers to process (1-indexed), None for all pages
            language: Language code for OCR (eng, fra, etc.)
            
        Returns:
            List of extracted text strings, one per page
            
        Raises:
            PDFReadError: If PDF cannot be read
            OCRError: If OCR processing fails
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
            
            logger.info(f"Extracting text from {len(pages_to_process)} pages in {language}")
            
            # Convert PDF pages to images
            images = self._convert_pdf_to_images(file_path, pages_to_process)
            
            # Extract text from images using OCR
            extracted_texts = []
            for i, image in enumerate(images):
                try:
                    page_num = pages_to_process[i]
                    logger.debug(f"Processing page {page_num}")
                    
                    # Configure OCR parameters
                    custom_config = f'--oem 3 --psm 6 -l {language}'
                    
                    # Extract text with confidence data
                    text_data = pytesseract.image_to_data(
                        image, 
                        lang=language, 
                        config=custom_config,
                        output_type=pytesseract.Output.DICT
                    )
                    
                    # Filter text by confidence threshold
                    filtered_text = self._filter_text_by_confidence(text_data)
                    extracted_texts.append(filtered_text)
                    
                    logger.debug(f"Extracted {len(filtered_text)} characters from page {page_num}")
                    
                except Exception as e:
                    logger.warning(f"OCR failed for page {page_num}: {str(e)}")
                    extracted_texts.append("")
            
            logger.info(f"Text extraction completed. Processed {len(extracted_texts)} pages")
            return extracted_texts
            
        except Exception as e:
            logger.error(f"Text extraction failed for {file_path}: {str(e)}")
            if isinstance(e, (PDFReadError, ValidationError)):
                raise
            raise OCRError(f"OCR processing failed: {str(e)}")
    
    def _convert_pdf_to_images(self, file_path: Path, pages: List[int]) -> List[Image.Image]:
        """Convert PDF pages to PIL Images.
        
        Args:
            file_path: Path to PDF file
            pages: List of page numbers (1-indexed)
            
        Returns:
            List of PIL Images
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_bytes = file.read()
            
            # Convert pages to images
            if len(pages) == 1:
                images = pdf2image.convert_from_bytes(
                    pdf_bytes, 
                    first_page=pages[0], 
                    last_page=pages[0],
                    dpi=300
                )
            else:
                images = pdf2image.convert_from_bytes(
                    pdf_bytes, 
                    first_page=min(pages), 
                    last_page=max(pages),
                    dpi=300
                )
                
                # Filter images for specific pages if needed
                if set(pages) != set(range(min(pages), max(pages) + 1)):
                    page_indices = [p - min(pages) for p in pages]
                    images = [images[i] for i in page_indices if i < len(images)]
            
            return images
            
        except Exception as e:
            raise OCRError(f"Failed to convert PDF to images: {str(e)}")
    
    def _filter_text_by_confidence(self, text_data: Dict[str, List]) -> str:
        """Filter OCR text by confidence threshold.
        
        Args:
            text_data: OCR output data from pytesseract
            
        Returns:
            Filtered text string
        """
        filtered_words = []
        
        for i, word in enumerate(text_data['text']):
            confidence = int(text_data['conf'][i])
            if confidence >= self.confidence_threshold and word.strip():
                filtered_words.append(word)
        
        return ' '.join(filtered_words)