# PDF to Text/Excel Converter

## Overview
This versatile web application allows users to convert PDF files to either text or Excel format, encapsulated within a Docker container. It features a user-friendly interface powered by Streamlit and leverages the pdf2image, pytesseract, PyPDF2, img2table, and paddleocr libraries for robust PDF processing capabilities.

## Prerequisites
Before running the application, ensure you have Docker installed on your machine.

## Usage
1. Build the Docker image:
   ```bash
   docker build -t pdf-to-excel-converter .
   
2. Run the Docker container:
   ```bash
   docker run -p 8501:8501 pdf-to-excel-converter
   
Access the application at http://localhost:8501 in your web browser.


## Instructions

1. Upload a PDF file using the provided file uploader.
2. View a preview of the PDF content by expanding the "Preview PDF content" section.
3. Choose the desired conversion type: Text or Excel.
4. Select the language for the OCR process: English or French.
5. Choose specific pages for conversion or leave blank to convert the entire document.
6. Click the "Convert" button to start the conversion process.
7. After conversion, a download button will appear, allowing you to download the resulting text or Excel file.

## Features
- PDF preview: Users can view their PDF before conversion.
- Language selection: Supports OCR in English and French.
- Page selection: Convert specific pages or the entire PDF.
- Dual conversion: Choose between text or Excel output.
- Downloadable results: Easily download the converted files.


## Support
If you find this project helpful, consider supporting the developer by [buying them a coffee](https://www.buymeacoffee.com/zakarialaktati)!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-yellow.svg)](https://www.buymeacoffee.com/zakarialaktati)
