import pytest
import os
import fitz
from utils.pdf_reader import extract_text_from_pdf
from services.document_service import process_document

def test_extract_pdf_text(tmp_path):
    """
    Verify text is extracted correctly page-by-page from a valid PDF.
    """
    pdf_path = os.path.join(tmp_path, "test.pdf")
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Hello, this is a test vocabulary context.")
    doc.save(pdf_path)
    doc.close()
    
    pages = extract_text_from_pdf(pdf_path)
    assert len(pages) == 1
    assert pages[0]["page_number"] == 1
    assert "test vocabulary context" in pages[0]["text"]

def test_extract_invalid_pdf(tmp_path):
    """
    Verify that trying to extract text from a malformed/invalid PDF raises an exception.
    """
    invalid_path = os.path.join(tmp_path, "invalid.pdf")
    with open(invalid_path, "w") as f:
        f.write("Not a PDF content")
        
    with pytest.raises(Exception):
        extract_text_from_pdf(invalid_path)

def test_process_document(tmp_path):
    """
    Verify document processing correctly bundles page text with filename metadata.
    """
    pdf_path = os.path.join(tmp_path, "test.pdf")
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Hello world from test document.")
    doc.save(pdf_path)
    doc.close()
    
    pages = process_document(pdf_path, "test_doc.pdf")
    assert len(pages) == 1
    assert pages[0]["filename"] == "test_doc.pdf"
    assert pages[0]["page_number"] == 1
    assert "Hello world" in pages[0]["text"]
