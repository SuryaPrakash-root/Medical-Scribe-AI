# Medical Scribe AI

Core intelligence engine for converting patient-doctor conversations into structured SOAP notes.

## Features

- **Automated Extraction**: Uses **Mistral AI (open-mistral-nemo)** to extract clinical data from transcripts.
- **Structured Output**: Generates strict JSON following SOAP format (Subjective, Objective, Assessment, Plan).
- **FastAPI Backend**: robust and easy-to-use API.
- **Frontend**: Glassmorphism UI for easy interaction.
- **Validation**: Pydantic models ensure data integrity.

## Setup

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Variables**:
    Create a `.env` file in the root directory and add your Mistral API key:
    ```
    MISTRAL_API_KEY=your_api_key_here
    ```

## Usage

1.  **Run the server**:
    ```bash
    uvicorn main:app --reload
    ```

2.  **Frontend**:
    Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Project Structure

- `main.py`: API entry point and static file server.
- `services.py`: Business logic and Mistral AI interaction.
- `schemas.py`: Data models.
- `static/`: Frontend files (HTML, CSS, JS).
