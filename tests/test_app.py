from streamlit.testing.v1 import AppTest

def test_app_startup():
    """
    Test that the Streamlit app starts up without exceptions
    and renders the primary headings and inputs.
    """
    at = AppTest.from_file("app.py")
    at.run()
    
    # Ensure no exceptions were raised during initialization
    assert not at.exception
    
    # Check main title and description
    assert at.title[0].body == "📚 AI Vocabulary Reader"
    
    # Check sidebar search widget is present
    assert len(at.sidebar.text_input) > 0
    assert at.sidebar.text_input[0].label == "Search vocabulary..."
    
    # Check form input labels
    assert len(at.text_input) > 0
    assert at.text_area[0].label == "Context"
