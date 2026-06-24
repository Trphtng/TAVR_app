import streamlit as st
from database.database import SessionLocal, init_db
from database.models import Vocabulary
from services.ai_service import analyze_word
from services.vocabulary_service import create_vocabulary, search_vocabulary, get_all_vocabulary
from services.learning_service import get_review_words, mark_easy, mark_hard

# Set page config
st.set_page_config(page_title="AI Vocabulary Reader", page_icon="📚", layout="wide")

# Initialize database tables
init_db()


# Custom premium styling via simple CSS inject
st.markdown("""
<style>
    .main {
        background-color: #fafafa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
    .vocab-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📚 AI Vocabulary Reader")
st.write("A personal local-first AI vocabulary app to translate, explain, and save technical terms.")

# Initialize session state for analyzed word data
if "analyzed_data" not in st.session_state:
    st.session_state.analyzed_data = None

# Sidebar for Search and History
st.sidebar.header("🔍 Search & History")
search_keyword = st.sidebar.text_input("Search vocabulary...", key="search_input")

# Fetch history inside sidebar using database session context
try:
    with SessionLocal() as db:
        if search_keyword.strip():
            saved_items = search_vocabulary(db, search_keyword.strip())
        else:
            saved_items = get_all_vocabulary(db)
            
    st.sidebar.subheader(f"Saved Items ({len(saved_items)})")
    
    # Render items list
    for item in reversed(saved_items):  # Newest first
        with st.sidebar.expander(f"📖 **{item.word}** ({item.topic or 'General'})"):
            st.write(f"**Translation:** {item.translation_vi}")
            st.write(f"**Technical:** {item.technical_en}")
            if item.context:
                st.info(f"**Context:** *{item.context}*")
            if item.source:
                st.caption(f"Source: {item.source}")
except Exception as e:
    st.sidebar.error(f"Failed to load vocabulary history: {e}")

# Main Content Area: Tabs for Analyze and Review Flashcards
tab_analyze, tab_learn = st.tabs(["🔍 Analyze & Browse", "🧠 Review Flashcards"])

with tab_analyze:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("Analyze New Word")
        
        # Selection of input method
        mode = st.radio("Input Method", ["Manual Input", "Upload PDF Document"], horizontal=True)
        
        word_val = ""
        context_val = ""
        default_source = ""
        
        if mode == "Upload PDF Document":
            uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
            if uploaded_file is not None:
                import tempfile
                import os
                from services.document_service import process_document
                from components.pdf_viewer import render_pdf_viewer
                
                # Save uploaded bytes to a temp file to allow PyMuPDF processing
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                    
                try:
                    pages = process_document(tmp_path, uploaded_file.name)
                    os.remove(tmp_path)
                    
                    if pages:
                        st.success(f"Processed {uploaded_file.name} ({len(pages)} pages)")
                        selected_word, extracted_context = render_pdf_viewer(pages)
                        
                        if selected_word:
                            word_val = selected_word
                            context_val = extracted_context
                        default_source = f"{uploaded_file.name} (Page {st.session_state.get('pdf_page_num', 1)})"
                except Exception as e:
                    st.error(f"Error processing PDF: {e}")
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
        
        # Inputs form
        with st.form("analyze_form"):
            word = st.text_input("Technical Word", value=word_val, placeholder="e.g. closure, decorator, database")
            context = st.text_area("Context", value=context_val, placeholder="Provide the sentence or context where you encountered the word...", height=120)
            source = st.text_input("Source Document / URL", value=default_source, placeholder="e.g. JavaScript Guide, page 42")
            
            submit_btn = st.form_submit_button("Analyze")
            
        if submit_btn:
            if not word.strip():
                st.error("Please provide a word to analyze.")
            else:
                with st.spinner("Analyzing with AI..."):
                    try:
                        # Execute service layer analysis
                        analysis = analyze_word(word.strip(), context.strip())
                        
                        # Merge UI inputs into the dictionary for persistence
                        analysis["context"] = context.strip()
                        analysis["source"] = source.strip()
                        
                        # Store in session state
                        st.session_state.analyzed_data = analysis
                        st.toast("Analysis finished!", icon="✅")
                    except Exception as e:
                        st.error(f"AI service failed: {e}")
                        st.session_state.analyzed_data = None
                        
    with col2:
        st.subheader("Bilingual Vocabulary Card")
        
        if st.session_state.analyzed_data:
            data = st.session_state.analyzed_data
            
            # UI Card Box
            from components.vocabulary_card import render_vocabulary_card
            render_vocabulary_card(data)
            
            # Save Action Button
            if st.button("Save to Vocabulary List"):
                try:
                    with SessionLocal() as db:
                        create_vocabulary(db, data)
                    st.success(f"Saved '{data.get('word')}' to database successfully!")
                    st.session_state.analyzed_data = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to save vocabulary: {e}")
        else:
            st.info("Enter a technical word on the left and click 'Analyze' to view the AI-generated card.")

with tab_learn:
    st.subheader("🧠 Spaced Repetition Learning")
    
    with SessionLocal() as db:
        due_words = get_review_words(db)
        
    if not due_words:
        st.success("🎉 You have reviewed all due words! Keep reading more documents to collect words.")
    else:
        st.info(f"You have **{len(due_words)}** words due for review.")
        
        active_vocab = due_words[0]
        
        if "card_revealed" not in st.session_state:
            st.session_state.card_revealed = False
            
        # Draw review flashcard
        st.markdown(f"""
        <div style="padding: 40px; border-radius: 12px; background-color: #f0f2f6; border: 2px solid #eaeaea; text-align: center; margin-bottom: 20px;">
            <span style="font-size: 14px; text-transform: uppercase; color: #555; font-weight: bold;">Word to review</span>
            <h1 style="margin: 10px 0; font-size: 42px; color: #1e1e1e;">{active_vocab.word}</h1>
            <p style="color: #666; font-style: italic;">Topic: {active_vocab.topic or 'General'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.card_revealed:
            if st.button("Reveal Answer", type="primary"):
                st.session_state.card_revealed = True
                st.rerun()
        else:
            st.markdown("### Answer Details")
            st.write(f"🇻🇳 **Vietnamese Translation:** {active_vocab.translation_vi}")
            st.write(f"🇬🇧 **English Translation:** {active_vocab.translation_en}")
            st.write(f"**Technical Explanation (EN):** {active_vocab.technical_en}")
            st.write(f"**Simple Explanation (EN):** {active_vocab.simple_en}")
            if active_vocab.context:
                st.info(f"**Context where encountered:** *{active_vocab.context}*")
                
            st.write("---")
            st.write("How was this word?")
            
            col_easy, col_hard = st.columns(2)
            with col_easy:
                if st.button("Easy 👍 (Space review further)", key="btn_easy"):
                    with SessionLocal() as db:
                        # Re-query the object in this session
                        vocab_db = db.query(Vocabulary).filter(Vocabulary.id == active_vocab.id).first()
                        if vocab_db:
                            mark_easy(db, vocab_db)
                    st.session_state.card_revealed = False
                    st.success("Marked as Easy!")
                    st.rerun()
            with col_hard:
                if st.button("Hard 👎 (Review again soon)", key="btn_hard"):
                    with SessionLocal() as db:
                        vocab_db = db.query(Vocabulary).filter(Vocabulary.id == active_vocab.id).first()
                        if vocab_db:
                            mark_hard(db, vocab_db)
                    st.session_state.card_revealed = False
                    st.warning("Marked as Hard!")
                    st.rerun()
