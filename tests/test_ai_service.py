import pytest
from unittest.mock import patch, MagicMock
from services.prompts import VOCAB_ANALYSIS_PROMPT_TEMPLATE
from utils.json_parser import extract_json
from services.ai_service import analyze_word

def test_prompt_generation():
    """
    Test that the prompt template embeds the word and context correctly.
    """
    word = "closure"
    context = "JavaScript closures are useful for data encapsulation."
    prompt = VOCAB_ANALYSIS_PROMPT_TEMPLATE.format(word=word, context=context)
    
    assert word in prompt
    assert context in prompt
    assert "translation_vi" in prompt
    assert "technical_explanation_en" in prompt

def test_json_parsing_markdown():
    """
    Test extraction of JSON from a markdown ```json ``` code block.
    """
    text_with_markdown = """
Here is the JSON response you requested:
```json
{
  "word": "closure",
  "translation_vi": "bao đóng",
  "translation_en": "closure",
  "technical_explanation_vi": "Một hàm có quyền truy cập vào phạm vi bên ngoài.",
  "technical_explanation_en": "A function referencing outer scope.",
  "simple_explanation_en": "A function that remembers variables.",
  "simple_explanation_vi": "Hàm ghi nhớ biến bên ngoài.",
  "example_en": "example()",
  "example_vi": "ví dụ",
  "topic": "Programming"
}
```
Hope this helps!
"""
    result = extract_json(text_with_markdown)
    assert result["word"] == "closure"
    assert result["topic"] == "Programming"

def test_json_parsing_plain():
    """
    Test parsing of a plain raw JSON string.
    """
    plain_text = """{
  "word": "closure",
  "translation_vi": "bao đóng",
  "translation_en": "closure",
  "technical_explanation_vi": "Một hàm có quyền truy cập vào phạm vi bên ngoài.",
  "technical_explanation_en": "A function referencing outer scope.",
  "simple_explanation_en": "A function that remembers variables.",
  "simple_explanation_vi": "Hàm ghi nhớ biến bên ngoài.",
  "example_en": "example()",
  "example_vi": "ví dụ",
  "topic": "Programming"
}"""
    result = extract_json(plain_text)
    assert result["word"] == "closure"

def test_json_parsing_invalid():
    """
    Test parsing error raising for malformed JSON text.
    """
    invalid_text = """
```json
{
  "word": "closure",
  "translation_vi": "bao đóng",
  # Invalid syntax
"""
    with pytest.raises(ValueError) as excinfo:
        extract_json(invalid_text)
    assert "Failed to parse JSON" in str(excinfo.value)

@patch("services.ai_service.genai.GenerativeModel")
@patch("services.ai_service.GEMINI_API_KEY", "mock_key")
def test_analyze_word_success(mock_model_class):
    """
    Test the main service function analyze_word with a mocked Gemini API.
    """
    mock_model_instance = MagicMock()
    mock_model_class.return_value = mock_model_instance
    
    mock_response = MagicMock()
    mock_response.text = """
```json
{
  "word": "closure",
  "translation_vi": "bao đóng",
  "translation_en": "closure",
  "technical_explanation_vi": "Bao đóng",
  "technical_explanation_en": "Closure",
  "simple_explanation_en": "Simple closure",
  "simple_explanation_vi": "Bao đóng đơn giản",
  "example_en": "example",
  "example_vi": "ví dụ",
  "topic": "Programming"
}
```
"""
    mock_model_instance.generate_content.return_value = mock_response
    
    with patch.dict("os.environ", {"AI_PROVIDER": "gemini"}):
        result = analyze_word("closure", "JavaScript closures are useful.")
        
    assert result["word"] == "closure"
    assert result["topic"] == "Programming"
    mock_model_instance.generate_content.assert_called_once()
