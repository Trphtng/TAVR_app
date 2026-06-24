import json
import re

def extract_json(text: str) -> dict:
    """
    Extracts and parses a JSON object from text.
    Handles ```json ... ``` blocks, raw JSON strings, and extra leading/trailing text.
    """
    text = text.strip()
    
    # Try finding markdown code block: ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # Try finding the first '{' and last '}'
        match_braces = re.search(r"(\{.*\})", text, re.DOTALL)
        if match_braces:
            json_str = match_braces.group(1)
        else:
            json_str = text
            
    # Clean up and parse
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from text: {e}\nRaw extracted text: {json_str}")
