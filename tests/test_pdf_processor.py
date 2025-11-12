"""
Unit tests for PDF processor functionality.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.core.pdf_processor import PDFProcessorImpl, TextExtractorImpl
from src.utils.exceptions import PDFReadError, ValidationError, OCRError


class TestPDFProcessorImpl:
    """Test cases for PDFProcessorImpl."""
    
    def test_init(self):
        """Test processor initialization."""
        processor = PDFProcessorImpl()
        assert processor is not None
    
    def test_init_with_tesseract_path(self):
        """Test processor initialization with tesseract path."""
        tesseract_path = "/usr/bin/tesseract"
        with patch('src.core.pdf_processor.pytesseract') as mock_pytesseract:
            processor = PDFProcessorImpl(tesseract_path)
            mock_pytesseract.pytesseract.tesseract_cmd = tesseract_path
            assert processor is not None
    
    def test_validate_file_success(self, sample_pdf_file: Path):
        """Test successful file validation."""
        processor = PDFProcessorImpl()
        
        with patch('src.core.pdf_processor.PdfReader') as mock_reader:
            mock_reader.return_value.pages = [Mock(), Mock()]  # 2 pages
            
            result = processor.validate_file(sample_pdf_file)
            assert result is True
    
    def test_validate_file_not_exists(self, temp_dir: Path):
        """Test validation of non-existent file."""
        processor = PDFProcessorImpl()
        non_existent = temp_dir / "does_not_exist.pdf"
        
        with pytest.raises(PDFReadError, match="File does not exist"):
            processor.validate_file(non_existent)
    
    def test_validate_file_wrong_extension(self, temp_dir: Path):
        """Test validation of file with wrong extension."""
        processor = PDFProcessorImpl()
        wrong_ext = temp_dir / "file.txt"
        wrong_ext.write_text("test")
        
        with pytest.raises(ValidationError, match="File is not a PDF"):
            processor.validate_file(wrong_ext)
    
    def test_validate_file_empty_pdf(self, sample_pdf_file: Path):
        """Test validation of PDF with no pages."""
        processor = PDFProcessorImpl()
        
        with patch('src.core.pdf_processor.PdfReader') as mock_reader:
            mock_reader.return_value.pages = []  # No pages
            
            with pytest.raises(PDFReadError, match="PDF file contains no pages"):
                processor.validate_file(sample_pdf_file)
    
    def test_get_page_count_success(self, sample_pdf_file: Path):
        """Test successful page count retrieval."""
        processor = PDFProcessorImpl()
        
        with patch('src.core.pdf_processor.PdfReader') as mock_reader:
            mock_reader.return_value.pages = [Mock(), Mock(), Mock()]  # 3 pages
            
            with patch.object(processor, 'validate_file', return_value=True):
                count = processor.get_page_count(sample_pdf_file)
                assert count == 3
    
    def test_get_page_count_invalid_file(self, invalid_pdf_file: Path):
        """Test page count with invalid file."""
        processor = PDFProcessorImpl()
        
        with pytest.raises(PDFReadError):
            processor.get_page_count(invalid_pdf_file)
    
    def test_extract_metadata_success(self, sample_pdf_file: Path):
        """Test successful metadata extraction."""
        processor = PDFProcessorImpl()
        
        mock_metadata = {
            '/Title': 'Test PDF',
            '/Author': 'Test Author',
            '/Creator': 'Test Creator'
        }
        
        with patch('src.core.pdf_processor.PdfReader') as mock_reader:
            mock_reader.return_value.pages = [Mock(), Mock()]
            mock_reader.return_value.metadata = mock_metadata
            
            with patch.object(processor, 'validate_file', return_value=True):
                metadata = processor.extract_metadata(sample_pdf_file)
                
                assert metadata['page_count'] == 2
                assert metadata['file_name'] == sample_pdf_file.name
                assert metadata['title'] == 'Test PDF'
                assert metadata['author'] == 'Test Author'
                assert 'file_size' in metadata


class TestTextExtractorImpl:
    """Test cases for TextExtractorImpl."""
    
    def test_init(self):
        """Test text extractor initialization."""
        extractor = TextExtractorImpl()
        assert extractor is not None
        assert extractor.confidence_threshold == 50
    
    def test_init_with_params(self):
        """Test text extractor initialization with parameters."""
        tesseract_path = "/usr/bin/tesseract"
        confidence = 70
        
        with patch('src.core.pdf_processor.pytesseract'):
            extractor = TextExtractorImpl(tesseract_path, confidence)
            assert extractor.confidence_threshold == 70
    
    @patch('src.core.pdf_processor.pdf2image.convert_from_bytes')
    @patch('src.core.pdf_processor.pytesseract.image_to_data')
    def test_extract_text_success(self, mock_ocr, mock_convert, sample_pdf_file: Path):
        """Test successful text extraction."""
        extractor = TextExtractorImpl()
        
        # Mock PDF conversion
        mock_image = Mock()
        mock_convert.return_value = [mock_image]
        
        # Mock OCR result
        mock_ocr_result = {
            'text': ['Hello', 'World', ''],
            'conf': ['85', '90', '0']
        }
        mock_ocr.return_value = mock_ocr_result
        
        # Mock PDF processor methods
        with patch.object(extractor.pdf_processor, 'validate_file', return_value=True):
            with patch.object(extractor.pdf_processor, 'get_page_count', return_value=1):
                
                result = extractor.extract_text(sample_pdf_file, language="eng")
                
                assert len(result) == 1
                assert "Hello World" in result[0]
                mock_convert.assert_called_once()
                mock_ocr.assert_called_once()
    
    def test_extract_text_invalid_pages(self, sample_pdf_file: Path):
        """Test text extraction with invalid page numbers."""
        extractor = TextExtractorImpl()
        
        with patch.object(extractor.pdf_processor, 'validate_file', return_value=True):
            with patch.object(extractor.pdf_processor, 'get_page_count', return_value=2):
                
                with pytest.raises(ValidationError, match="Invalid page numbers"):
                    extractor.extract_text(sample_pdf_file, pages=[0, 5])  # Invalid pages
    
    def test_filter_text_by_confidence(self):
        """Test text filtering by confidence threshold."""
        extractor = TextExtractorImpl(confidence_threshold=60)
        
        text_data = {
            'text': ['Good', 'Bad', 'Excellent', ''],
            'conf': ['70', '30', '90', '0']
        }
        
        result = extractor._filter_text_by_confidence(text_data)
        assert result == "Good Excellent"
    
    @patch('src.core.pdf_processor.pdf2image.convert_from_bytes')
    def test_convert_pdf_to_images_single_page(self, mock_convert, sample_pdf_file: Path):
        """Test PDF to images conversion for single page."""
        extractor = TextExtractorImpl()
        mock_image = Mock()
        mock_convert.return_value = [mock_image]
        
        with open(sample_pdf_file, 'rb') as f:
            result = extractor._convert_pdf_to_images(sample_pdf_file, [1])
            
            assert len(result) == 1
            mock_convert.assert_called_once()
    
    def test_convert_pdf_to_images_failure(self, sample_pdf_file: Path):
        """Test PDF to images conversion failure."""
        extractor = TextExtractorImpl()
        
        with patch('src.core.pdf_processor.pdf2image.convert_from_bytes', side_effect=Exception("Conversion failed")):
            with pytest.raises(OCRError, match="Failed to convert PDF to images"):
                extractor._convert_pdf_to_images(sample_pdf_file, [1])