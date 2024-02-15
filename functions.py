import pdf2image
import pytesseract
from PyPDF2 import PdfReader
from tempfile import NamedTemporaryFile
from pdf2image import convert_from_path
from img2table.ocr import PaddleOCR
from img2table.document import PDF

# Function to convert PDF to text
def convert_pdf_to_text(pdf_file_path, language, selected_pages=None):
    # Set language for OCR
    lang = 'eng' if language == 'English' else 'fra'
    # Read PDF file as bytes
    with open(pdf_file_path, 'rb') as file:
        pdf_bytes = file.read()
    # Convert selected pages to images
    if selected_pages is None or len(selected_pages) == 0:
        images = pdf2image.convert_from_bytes(pdf_bytes)
    else:
        images = pdf2image.convert_from_bytes(pdf_bytes, first_page=min(selected_pages), last_page=max(selected_pages))
    # Use OCR to convert images to text
    texts = [pytesseract.image_to_string(image, lang=lang) for image in images]
    return texts, len(images)

# Function to get the total number of pages in the PDF
def get_total_pages(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        return len(pdf_reader.pages)
# Function to convert PDF to Excel
def convert_pdf_to_excel(pdf_file_path, language, selected_pages=None):
    # Set language for OCR
    lang = 'en' if language == 'English' else 'fr'
    
    # Check if selected_pages is None, and handle accordingly
    if selected_pages is None:
        selected_pages = []

    # Convert selected pages to images
    if len(selected_pages) == 0:
        images = convert_from_path(pdf_file_path)
    else:
        images = convert_from_path(pdf_file_path, first_page=min(selected_pages), last_page=max(selected_pages))

    # Initialize PaddleOCR
    paddle_ocr = PaddleOCR(lang=lang, kw={"use_dilation": True})
    
    # Initialize the PDF document
    doc = PDF(pdf_file_path, pages=[page - 1 for page in selected_pages], detect_rotation=False, pdf_text_extraction=True)
    
    # Extract tables
    extracted_tables = doc.extract_tables(ocr=paddle_ocr, implicit_rows=False, borderless_tables=False, min_confidence=50)
    
    # Save Excel file to a temporary file
    with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmpfile:
        excel_file_path = tmpfile.name
        doc.to_xlsx(excel_file_path, ocr=paddle_ocr, implicit_rows=False, borderless_tables=False, min_confidence=50)
    
    return excel_file_path, extracted_tables
