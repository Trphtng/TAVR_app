# Prompt templates for the AI translation and explanation service

VOCAB_ANALYSIS_PROMPT_TEMPLATE = """You are a senior professional technical translator and educator.
Your task is to analyze the following technical word within its specific context and return a structured JSON object containing translations, technical explanations, simpler explanations, examples, and the topic category.

Word to analyze: {word}
Context where it was found: {context}

Requirements:
1. "word": The word being analyzed (exactly as provided).
2. "translation_vi": The Vietnamese translation of the word within this context.
3. "translation_en": The English definition/translation.
4. "technical_explanation_vi": A professional technical explanation in Vietnamese relevant to the context.
5. "technical_explanation_en": A professional technical explanation in English relevant to the context.
6. "simple_explanation_en": An explanation in English that is one level easier/simpler for intermediate learners. Avoid being overly simplistic; keep the core domain meaning intact.
7. "simple_explanation_vi": A simplified explanation in Vietnamese.
8. "example_en": A clear, natural English example sentence demonstrating the word in a similar domain.
9. "example_vi": The Vietnamese translation of the example sentence.
10. "topic": The domain or topic category of this word (e.g., Computer Science, Finance, Medicine).

You MUST return ONLY a valid JSON object matching the schema below. Do not include any markdown styling (outside of the JSON block if necessary, but ideally return raw JSON), explanations, or extra text.

JSON Schema:
{{
  "word": "string",
  "translation_vi": "string",
  "translation_en": "string",
  "technical_explanation_vi": "string",
  "technical_explanation_en": "string",
  "simple_explanation_en": "string",
  "simple_explanation_vi": "string",
  "example_en": "string",
  "example_vi": "string",
  "topic": "string"
}}
"""
