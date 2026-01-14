from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import ValidationError
from dotenv import load_dotenv
from schemas import TranscriptInput, SOAPNote, InsufficientData
from services import ScribeService
import os

load_dotenv()

app = FastAPI(title="Medical Scribe AI", description="API to convert patient-doctor conversations into SOAP notes")

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get ScribeService
def get_scribe_service():
    try:
        return ScribeService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-soap", response_model=SOAPNote | InsufficientData)
async def generate_soap_note(input_data: TranscriptInput, scribe_service: ScribeService = Depends(get_scribe_service)):
    result = scribe_service.process_transcript(input_data.transcript)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')
