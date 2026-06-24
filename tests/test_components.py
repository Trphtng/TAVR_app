from components.pdf_viewer import extract_context_sentence

def test_extract_context_sentence_found():
    """
    Verify that context sentence is correctly extracted when target word is present.
    """
    text = "Python decorators are a clean way to wrap functions. JavaScript closures are useful for data encapsulation."
    context = extract_context_sentence("closures", text)
    assert context == "JavaScript closures are useful for data encapsulation."

def test_extract_context_sentence_case_insensitive():
    """
    Verify context sentence extraction is case insensitive.
    """
    text = "Python Decorators are a clean way to wrap functions."
    context = extract_context_sentence("decorators", text)
    assert context == "Python Decorators are a clean way to wrap functions."

def test_extract_context_sentence_not_found():
    """
    Verify that an empty string is returned if the word is not in the text.
    """
    text = "Python decorators are a clean way to wrap functions."
    context = extract_context_sentence("closures", text)
    assert context == ""
