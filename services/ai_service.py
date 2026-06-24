import os
from google import genai
from config import GEMINI_API_KEY, AI_PROVIDER
from services.prompts import VOCAB_ANALYSIS_PROMPT_TEMPLATE
from utils.json_parser import extract_json

def analyze_word(word: str, context: str) -> dict:
    """
    Analyzes a technical word within its context using the configured AI provider.
    Returns a dictionary matching the vocabulary schema.
    """
    provider = os.getenv("AI_PROVIDER", AI_PROVIDER).lower()
    prompt = VOCAB_ANALYSIS_PROMPT_TEMPLATE.format(word=word, context=context)
    
    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
        if not api_key or api_key == "your_api_key_here":
            raise ValueError("GEMINI_API_KEY is not configured or is using the placeholder value.")
        
        client = genai.Client(api_key=api_key)
        # Using gemini-1.5-flash as the default fast text generation model
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        response_text = response.text

    else:
        raise ValueError(f"Unsupported AI provider: {provider}")
        
    # Extract and parse JSON
    parsed_json = extract_json(response_text)
    
    # Validate and normalize keys in the output
    required_keys = [
        "word", "translation_vi", "translation_en",
        "technical_explanation_vi", "technical_explanation_en",
        "simple_explanation_en", "simple_explanation_vi",
        "example_en", "example_vi", "topic"
    ]
    for key in required_keys:
        if key not in parsed_json:
            parsed_json[key] = ""
            
    return parsed_json
