import streamlit as st
from functions import convert_pdf_to_text, convert_pdf_to_excel, get_total_pages
from tempfile import NamedTemporaryFile
import base64

st.set_page_config(page_title="PDF Converter")

st.title("PDF Converter")

# Upload PDF file
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

def display_pdf(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

if pdf_file is not None:
    # Display PDF inside an expander
    with st.expander("Preview PDF content"):
        display_pdf(pdf_file)
        pdf_file.seek(0)  # Reset file pointer to the beginning

    # Save PDF file to a temporary file
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        tmpfile.write(pdf_file.read())
        pdf_file_path = tmpfile.name

    # Allow user to choose between Excel and Text conversion
    conversion_option = st.selectbox("Select conversion type", ["Text", "Excel"])
    language_option = st.selectbox("Select language", ["English", "French"])
    total_pages = get_total_pages(pdf_file_path)
    page_selection = st.multiselect("Select pages to convert (None for all)", list(range(1, total_pages + 1)), default=None)


    if st.button("Convert"):
        if conversion_option == "Text":
            # Convert PDF to text
            texts, num_pages = convert_pdf_to_text(pdf_file_path, language_option, page_selection)
            st.header("Extracted Text")
            st.text(f"Total number of pages: {num_pages}")
            for page_num, text_content in enumerate(texts):
                st.subheader(f"Page {page_num + 1}")
                st.text(text_content)
            # Download button for text
            st.download_button(label="Download Text File",
                               data="\n\n".join(texts),
                               file_name="output.txt",
                               mime="text/plain")

        elif conversion_option == "Excel":
            # Convert PDF to Excel
            excel_file_path, _ = convert_pdf_to_excel(pdf_file_path, language_option, page_selection)
            st.success("Excel file generated successfully!")
            # Download button for Excel
            with open(excel_file_path, "rb") as file:
                st.download_button(label="Download Excel File",
                                   data=file.read(),
                                   file_name="output.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")