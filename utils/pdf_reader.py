import fitz

def extract_text_from_pdf(path: str) -> list:
    """
    Extracts text page-by-page from a PDF file using PyMuPDF (fitz).
    Returns a list of dictionaries, where each dict has:
    - "page_number": int (1-indexed)
    - "text": str
    """
    doc = fitz.open(path)
    pages = []
    try:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            pages.append({
                "page_number": page_num + 1,
                "text": text
            })
    finally:
        doc.close()
    return pages
