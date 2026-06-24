from utils.pdf_reader import extract_text_from_pdf

def process_document(file_path: str, filename: str) -> list:
    """
    Processes a document (like a PDF) to extract text page-by-page.
    Appends metadata such as filename.
    Returns a list of dictionaries with page_number, text, and filename keys.
    """
    pages = extract_text_from_pdf(file_path)
    for page in pages:
        page["filename"] = filename
    return pages
