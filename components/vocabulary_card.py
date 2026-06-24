import streamlit as st

def render_vocabulary_card(data: dict) -> None:
    """
    Renders the AI-analyzed vocabulary card with detailed explanations,
    translations, and example sentences.
    """
    if not data:
        return
        
    # Card wrapper styling
    st.markdown(f"""
    <div class="vocab-card" style="padding: 20px; border-radius: 12px; background-color: #ffffff; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 20px;">
        <h3>{data.get('word')}</h3>
        <p><strong>Topic:</strong> {data.get('topic', 'General')}</p>
    </div>
    """, unsafe_allow_html=True)
    
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
