"""
Unit tests for file validation functionality.
"""

import pytest
import io
from pathlib import Path

from src.core.file_validator import FileValidatorImpl
from src.utils.exceptions import ValidationError


class TestFileValidatorImpl:
    """Test cases for FileValidatorImpl."""
    
    def test_init_default(self):
        """Test validator initialization with defaults."""
        validator = FileValidatorImpl()
        assert validator.allowed_extensions == ['.pdf']
    
    def test_init_custom_extensions(self):
        """Test validator initialization with custom extensions."""
        extensions = ['.pdf', '.docx', '.txt']
        validator = FileValidatorImpl(extensions)
        assert validator.allowed_extensions == extensions
    
    def test_validate_file_type_valid_pdf(self, sample_pdf_io: io.BytesIO):
        """Test validation of valid PDF file type."""
        validator = FileValidatorImpl()
        
        result = validator.validate_file_type(sample_pdf_io)
        assert result is True
    
    def test_validate_file_type_invalid(self):
        """Test validation of invalid file type."""
        validator = FileValidatorImpl()
        invalid_file = io.BytesIO(b"This is not a PDF")
        
        with pytest.raises(ValidationError, match="File is not a valid PDF"):
            validator.validate_file_type(invalid_file)
    
    def test_validate_file_size_valid(self):
        """Test validation of valid file size."""
        validator = FileValidatorImpl()
        
        # Create a small file (1KB)
        small_file = io.BytesIO(b"x" * 1024)
        
        result = validator.validate_file_size(small_file, max_size_mb=1)
        assert result is True
    
    def test_validate_file_size_too_large(self):
        """Test validation of file that's too large."""
        validator = FileValidatorImpl()
        
        # Create a large file (2MB)
        large_file = io.BytesIO(b"x" * (2 * 1024 * 1024))
        
        with pytest.raises(ValidationError, match="exceeds maximum allowed size"):
            validator.validate_file_size(large_file, max_size_mb=1)
    
    def test_validate_filename_valid(self):
        """Test validation of valid filename."""
        validator = FileValidatorImpl()
        
        result = validator.validate_filename("document.pdf")
        assert result is True
    
    def test_validate_filename_empty(self):
        """Test validation of empty filename."""
        validator = FileValidatorImpl()
        
        with pytest.raises(ValidationError, match="Filename cannot be empty"):
            validator.validate_filename("")
    
    def test_validate_filename_wrong_extension(self):
        """Test validation of filename with wrong extension."""
        validator = FileValidatorImpl()
        
        with pytest.raises(ValidationError, match="File extension '.txt' not allowed"):
            validator.validate_filename("document.txt")
    
    def test_validate_filename_dangerous_characters(self):
        """Test validation of filename with dangerous characters."""
        validator = FileValidatorImpl()
        
        dangerous_names = [
            "../document.pdf",
            "document/path.pdf",
            "document\\path.pdf",
            "document:path.pdf",
            "document*.pdf",
            "document?.pdf",
            'document"path.pdf',
            "document<path.pdf",
            "document>path.pdf",
            "document|path.pdf"
        ]
        
        for dangerous_name in dangerous_names:
            with pytest.raises(ValidationError, match="contains invalid characters"):
                validator.validate_filename(dangerous_name)
    
    def test_validate_file_size_preserves_position(self):
        """Test that file size validation preserves file position."""
        validator = FileValidatorImpl()
        
        file_content = b"x" * 1024
        test_file = io.BytesIO(file_content)
        
        # Move to middle of file
        test_file.seek(512)
        original_position = test_file.tell()
        
        # Validate file size
        validator.validate_file_size(test_file, max_size_mb=1)
        
        # Check that position is preserved
        assert test_file.tell() == original_position
    
    def test_validate_file_type_preserves_position(self, sample_pdf_io: io.BytesIO):
        """Test that file type validation preserves file position."""
        validator = FileValidatorImpl()
        
        # Move to middle of file
        sample_pdf_io.seek(100)
        original_position = sample_pdf_io.tell()
        
        # Validate file type
        validator.validate_file_type(sample_pdf_io)
        
        # Check that position is preserved
        assert sample_pdf_io.tell() == original_position