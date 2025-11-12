"""
Base interfaces for PDF processing operations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import io

class PDFProcessor(ABC):
    """Abstract base class for PDF processors."""
    
    @abstractmethod
    def validate_file(self, file_path: Path) -> bool:
        """Validate PDF file."""
        pass
    
    @abstractmethod
    def get_page_count(self, file_path: Path) -> int:
        """Get total number of pages in PDF."""
        pass
    
    @abstractmethod
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract PDF metadata."""
        pass

class TextExtractor(ABC):
    """Abstract base class for text extraction."""
    
    @abstractmethod
    def extract_text(
        self, 
        file_path: Path, 
        pages: Optional[List[int]] = None,
        language: str = "eng"
    ) -> List[str]:
        """Extract text from PDF pages."""
        pass

class TableExtractor(ABC):
    """Abstract base class for table extraction."""
    
    @abstractmethod
    def extract_tables(
        self, 
        file_path: Path, 
        pages: Optional[List[int]] = None,
        language: str = "eng"
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Extract tables from PDF and save as Excel."""
        pass

class FileValidator(ABC):
    """Abstract base class for file validation."""
    
    @abstractmethod
    def validate_file_type(self, file: io.BytesIO) -> bool:
        """Validate file type."""
        pass
    
    @abstractmethod
    def validate_file_size(self, file: io.BytesIO, max_size_mb: int) -> bool:
        """Validate file size."""
        pass