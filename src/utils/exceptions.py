"""
Custom exceptions for PDF processing operations.
"""

class PDFProcessingError(Exception):
    """Base exception for PDF processing errors."""
    pass

class PDFReadError(PDFProcessingError):
    """Raised when PDF file cannot be read or is corrupted."""
    pass

class OCRError(PDFProcessingError):
    """Raised when OCR processing fails."""
    pass

class ConversionError(PDFProcessingError):
    """Raised when conversion process fails."""
    pass

class ValidationError(PDFProcessingError):
    """Raised when input validation fails."""
    pass

class ConfigurationError(PDFProcessingError):
    """Raised when configuration is invalid."""
    pass