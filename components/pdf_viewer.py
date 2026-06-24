import streamlit as st
import re

def extract_context_sentence(word: str, text: str) -> str:
    """
    Extracts the sentence containing the target word from the text.
    """
    # Split text into sentences using simple regex punctuation markers
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for sentence in sentences:
        if re.search(rf"\b{re.escape(word)}\b", sentence, re.IGNORECASE):
            return sentence.strip()
    return ""

def render_pdf_viewer(pages: list) -> tuple:
    """
    Renders the PDF viewer component in Streamlit.
    Allows browsing pages, selecting a word from the page text,
    and automatically extracting the sentence context.
    Returns a tuple of (selected_word, extracted_context).
    """
    if not pages:
        return "", ""
        
    st.subheader("📄 Document Viewer")
    
    # Page selector
    page_num = st.number_input("Go to Page", min_value=1, max_value=len(pages), value=1, key="pdf_page_num")
    page_data = pages[page_num - 1]
    page_text = page_data["text"]
    
    # Display page text
    st.text_area("Page Text Content", value=page_text, height=250, disabled=True, key="pdf_text_display")
    
    # Find list of alphanumeric words longer than 2 characters
    words = re.findall(r"\b[a-zA-Z]{3,}\b", page_text)
    unique_words = sorted(list(set(words)))
    
    selected_word = st.selectbox("Select a word to analyze from this page:", [""] + unique_words, key="pdf_selected_word")
    
    extracted_context = ""
    if selected_word:
        extracted_context = extract_context_sentence(selected_word, page_text)
        if extracted_context:
            st.info(f"**Extracted Context:** *{extracted_context}*")
            
    return selected_word, extracted_context
