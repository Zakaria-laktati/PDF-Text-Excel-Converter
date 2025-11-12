"""
File validation utilities.
"""

import io
from pathlib import Path
from typing import List

from src.core.interfaces import FileValidator
from src.utils.exceptions import ValidationError
from src.utils.logger import get_logger

logger = get_logger(__name__)

class FileValidatorImpl(FileValidator):
    """Implementation of file validation."""
    
    def __init__(self, allowed_extensions: List[str] = None):
        """Initialize file validator.
        
        Args:
            allowed_extensions: List of allowed file extensions (default: ['.pdf'])
        """
        self.allowed_extensions = allowed_extensions or ['.pdf']
        logger.info(f"File validator initialized with extensions: {self.allowed_extensions}")
    
    def validate_file_type(self, file: io.BytesIO) -> bool:
        """Validate file type by checking magic bytes.
        
        Args:
            file: File-like object to validate
            
        Returns:
            True if file type is valid
            
        Raises:
            ValidationError: If file type is invalid
        """
        try:
            # Save current position
            current_pos = file.tell()
            
            # Read first few bytes to check magic number
            file.seek(0)
            header = file.read(8)
            
            # Restore position
            file.seek(current_pos)
            
            # Check PDF magic number
            if header.startswith(b'%PDF-'):
                logger.debug("Valid PDF file detected")
                return True
            
            # Check for other formats if needed
            # Add more magic number checks here
            
            raise ValidationError("File is not a valid PDF")
            
        except Exception as e:
            logger.error(f"File type validation failed: {str(e)}")
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Cannot validate file type: {str(e)}")
    
    def validate_file_size(self, file: io.BytesIO, max_size_mb: int) -> bool:
        """Validate file size.
        
        Args:
            file: File-like object to validate
            max_size_mb: Maximum allowed size in MB
            
        Returns:
            True if file size is valid
            
        Raises:
            ValidationError: If file size is too large
        """
        try:
            # Save current position
            current_pos = file.tell()
            
            # Get file size
            file.seek(0, 2)  # Seek to end
            file_size = file.tell()
            
            # Restore position
            file.seek(current_pos)
            
            # Convert to MB
            file_size_mb = file_size / (1024 * 1024)
            
            logger.debug(f"File size: {file_size_mb:.2f} MB (limit: {max_size_mb} MB)")
            
            if file_size_mb > max_size_mb:
                raise ValidationError(
                    f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed size ({max_size_mb} MB)"
                )
            
            return True
            
        except Exception as e:
            logger.error(f"File size validation failed: {str(e)}")
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Cannot validate file size: {str(e)}")
    
    def validate_filename(self, filename: str) -> bool:
        """Validate filename and extension.
        
        Args:
            filename: Name of the file
            
        Returns:
            True if filename is valid
            
        Raises:
            ValidationError: If filename is invalid
        """
        try:
            if not filename:
                raise ValidationError("Filename cannot be empty")
            
            # Check file extension
            file_path = Path(filename)
            extension = file_path.suffix.lower()
            
            if extension not in self.allowed_extensions:
                raise ValidationError(
                    f"File extension '{extension}' not allowed. "
                    f"Allowed extensions: {', '.join(self.allowed_extensions)}"
                )
            
            # Check for potentially dangerous characters
            dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
            if any(char in filename for char in dangerous_chars):
                raise ValidationError("Filename contains invalid characters")
            
            logger.debug(f"Filename validation passed: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Filename validation failed for '{filename}': {str(e)}")
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Invalid filename: {str(e)}")