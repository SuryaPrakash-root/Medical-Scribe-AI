from mistralai import Mistral
import os
import json
from schemas import SOAPNote, InsufficientData

class ScribeService:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY is not set in environment variables")
        self.client = Mistral(api_key=self.api_key)
        self.model = "open-mistral-nemo"  # Using the model that worked: open-mistral-nemo

    def process_transcript(self, transcript: str):
        system_prompt = """
        You are an expert medical scribe. Your task is to convert raw patient-doctor conversations into professional SOAP notes.
        
        Strictly follow this JSON structure:
        {
          "subjective": { "chief_complaint": "string", "hpi": "string" },
          "objective": { "exam": "string", "vitals": "string", "labs": "string" },
          "assessment": ["string", "string"],
          "plan": {
            "medications": ["string"],
            "labs": ["string"],
            "referrals": ["string"],
            "instructions": ["string"],
            "follow_up": "string"
          },
          "visit_summary": "string"
        }

        Rules:
        1. Extract clinical data accurately.
        2. use professional medical terminology.
        3. If there is insufficient clinical data to form a SOAP note (e.g., just greetings, or non-medical talk), return:
           { "status": "insufficient_clinical_data" }
        4. Do NOT output markdown or conversational text. Output ONLY the JSON object.
        5. "assessment" must be a list of strings.
        6. "plan" fields must be lists where specified.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Transcript:\n{transcript}"}
        ]

        try:
            chat_response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            content = chat_response.choices[0].message.content
            data = json.loads(content)
            
            if "status" in data and data["status"] == "insufficient_clinical_data":
                return InsufficientData(status="insufficient_clinical_data")
            
            # Validate against SOAPNote schema
            return SOAPNote(**data)
            
        except json.JSONDecodeError:
             return {"error": "Failed to parse LLM response as JSON"}
        except Exception as e:
            return {"error": str(e)}
