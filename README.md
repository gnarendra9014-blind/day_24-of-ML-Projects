# Day 24: LLM API

This project provides a simple, rate-limited, and authenticated API built with FastAPI that acts as an interface to an underlying Large Language Model (Google Gemini).

## Features

- **FastAPI Framework**: Fast, asynchronous web framework.
- **Authentication**: Simple API key based authentication.
- **Rate Limiting**: Protects endpoints from abuse using in-memory rate limiting.
- **Logging**: Comprehensive logging of API requests, responses, and errors.
- **Gemini Integration**: Connects to the Google Gemini API for chat completions.
- **Testing**: Includes test scripts to verify endpoints and rate limiting.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gnarendra9014-blind/day_24-of-ML-Projects.git
   cd day_24-of-ML-Projects
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   API_KEY=your_secure_api_key
   ```

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## Testing

Run the test script to verify authentication, chat completion, and rate limiting:
```bash
python test_api.py
```
