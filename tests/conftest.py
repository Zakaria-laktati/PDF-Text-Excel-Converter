"""
Test configuration and fixtures.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator
import io

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "test_data"

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def sample_pdf_bytes() -> bytes:
    """Create a minimal valid PDF for testing."""
    # Minimal PDF content
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Hello World) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000204 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
297
%%EOF"""
    return pdf_content

@pytest.fixture
def sample_pdf_file(temp_dir: Path, sample_pdf_bytes: bytes) -> Path:
    """Create a sample PDF file for testing."""
    pdf_path = temp_dir / "sample.pdf"
    pdf_path.write_bytes(sample_pdf_bytes)
    return pdf_path

@pytest.fixture
def invalid_pdf_file(temp_dir: Path) -> Path:
    """Create an invalid PDF file for testing."""
    invalid_path = temp_dir / "invalid.pdf"
    invalid_path.write_text("This is not a PDF file")
    return invalid_path

@pytest.fixture
def sample_pdf_io(sample_pdf_bytes: bytes) -> io.BytesIO:
    """Create a BytesIO object with PDF content."""
    return io.BytesIO(sample_pdf_bytes)