# AI Vocabulary Reader

A personal, local-first AI vocabulary application designed to help users learn and retain technical terminology from documents.

## Project Goal
To provide a clean, local-first utility where users can select technical words from documents, get AI-powered translations and context-aware explanations, generate bilingual vocabulary cards, and manage their personal local vocabulary database.

## Architecture & Structure
The project is organized following clean architectural patterns:
* `database/` - SQLAlchemy models and local SQLite database session management.
* `services/` - Core business services including local vocabulary management and Gemini API/Ollama integrations.
* `utils/` - Shared utilities like exporting vocabulary to CSV/JSON.
* `tests/` - Unit and integration tests.
* `data/` - Storage location for the local SQLite database.

## Prerequisites
* Python 3.11 or higher
* A Gemini API key (or local Ollama setup)

## Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AI-Vocabulary-Reader
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy the example environment file and add your credentials:
   ```bash
   cp .env.example .env
   # Edit .env and enter your actual GEMINI_API_KEY
   ```

## Running the Application

*(Streamlit UI will be implemented in Phase 1)*

To start the application:
```bash
streamlit run app.py
```

## Running Tests
To run the test suite:
```bash
pytest
```
