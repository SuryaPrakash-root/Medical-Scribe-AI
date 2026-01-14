from typing import List, Optional
from pydantic import BaseModel, Field

class Subjective(BaseModel):
    chief_complaint: str = Field(..., description="The patient's primary complaint")
    hpi: str = Field(..., description="History of present illness")

class Objective(BaseModel):
    exam: str = Field(..., description="Physical exam findings")
    vitals: str = Field(..., description="Vital signs if mentioned")
    labs: str = Field(..., description="Lab results if mentioned")

class Plan(BaseModel):
    medications: List[str] = Field(default_factory=list, description="List of medications prescribed or adjusted")
    labs: List[str] = Field(default_factory=list, description="List of labs ordered")
    referrals: List[str] = Field(default_factory=list, description="List of referrals made")
    instructions: List[str] = Field(default_factory=list, description="Patient instructions")
    follow_up: str = Field(..., description="Follow-up instructions")

class SOAPNote(BaseModel):
    subjective: Subjective
    objective: Objective
    assessment: List[str] = Field(..., description="List of assessments or diagnoses")
    plan: Plan
    visit_summary: str = Field(..., description="Concise summary of the visit")

class InsufficientData(BaseModel):
    status: str = "insufficient_clinical_data"

class TranscriptInput(BaseModel):
    transcript: str
