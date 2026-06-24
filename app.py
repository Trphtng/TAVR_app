import streamlit as st
from database.database import SessionLocal
from services.ai_service import analyze_word
from services.vocabulary_service import create_vocabulary, search_vocabulary, get_all_vocabulary

# Set page config
st.set_page_config(page_title="AI Vocabulary Reader", page_icon="📚", layout="wide")

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

# Layout: Main input and main output side-by-side
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("Analyze New Word")
    
    # Selection of input method
    mode = st.radio("Input Method", ["Manual Input", "Upload PDF Document"], horizontal=True)
    
    default_source = ""
    
    if mode == "Upload PDF Document":
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            import tempfile
            import os
            from services.document_service import process_document
            
            # Save uploaded bytes to a temp file to allow PyMuPDF processing
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
                
            try:
                pages = process_document(tmp_path, uploaded_file.name)
                os.remove(tmp_path)
                
                if pages:
                    st.success(f"Processed {uploaded_file.name} ({len(pages)} pages)")
                    page_num = st.number_input("Select Page", min_value=1, max_value=len(pages), value=1)
                    page_data = pages[page_num - 1]
                    
                    st.text_area("Page Text Content", value=page_data["text"], height=150, disabled=True)
                    default_source = f"{uploaded_file.name} (Page {page_num})"
            except Exception as e:
                st.error(f"Error processing PDF: {e}")
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
    
    # Inputs form
    with st.form("analyze_form"):
        word = st.text_input("Technical Word", placeholder="e.g. closure, decorator, database")
        context = st.text_area("Context", placeholder="Provide the sentence or context where you encountered the word...", height=120)
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
        st.markdown(f"""
        <div class="vocab-card">
            <h3>{data.get('word')}</h3>
            <p><strong>Topic:</strong> {data.get('topic', 'General')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for translations, explanations, and examples
        tab1, tab2, tab3 = st.tabs(["Translations", "Explanations", "Examples"])
        
        with tab1:
            st.write(f"🇻🇳 **Vietnamese Translation:** {data.get('translation_vi')}")
            st.write(f"🇬🇧 **English Translation:** {data.get('translation_en')}")
            
        with tab2:
            st.write(f"**Technical Explanation (EN):** {data.get('technical_explanation_en')}")
            st.write(f"**Technical Explanation (VI):** {data.get('technical_explanation_vi')}")
            st.write(f"**Simple Explanation (EN):** {data.get('simple_explanation_en')}")
            st.write(f"**Simple Explanation (VI):** {data.get('simple_explanation_vi')}")
            
        with tab3:
            st.write(f"**Example Sentence (EN):** *{data.get('example_en')}*")
            st.write(f"**Example Sentence (VI):** *{data.get('example_vi')}*")
            
        st.write(" ")
        
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
