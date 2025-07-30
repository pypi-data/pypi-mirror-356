from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date
from .base import BaseSchema

class Education(BaseModel):
    school_name: str = Field(..., description="Name of school/college")
    degree: str = Field(..., description="Degree/certificate obtained")
    field: str = Field(..., description="Field of study")
    years_attended: str = Field(..., description="Years attended (e.g., 2015-2019)")
    graduated: bool = Field(False, description="Did you graduate?")

class EmploymentHistory(BaseModel):
    employer: str = Field(..., description="Employer name")
    position: str = Field(..., description="Job title/position")
    start_date: str = Field(..., description="Start date (MM/YYYY)")
    end_date: str = Field("Present", description="End date (MM/YYYY) or 'Present'")
    responsibilities: List[str] = Field(..., description="List of responsibilities and achievements")
    supervisor: str = Field("", description="Supervisor name")
    phone: str = Field("", description="Employer phone number")
    address: str = Field("", description="Employer address")
    reason_for_leaving: str = Field("", description="Reason for leaving")

class Reference(BaseModel):
    name: str = Field(..., description="Reference name")
    relationship: str = Field(..., description="Relationship to applicant")
    company: str = Field("", description="Company name")
    phone: str = Field(..., description="Phone number")
    email: EmailStr = Field(..., description="Email address")

class JobApplicationSchema(BaseModel):
    # Personal Information
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    zip_code: str = Field(..., description="ZIP code")
    phone: str = Field(..., description="Primary phone number")
    email: EmailStr = Field(..., description="Email address")
    ssn: str = Field("", description="Social Security Number (if required)")
    position: str = Field(..., description="Position applied for")
    available_start_date: str = Field(..., description="Date available to start (MM/DD/YYYY)")
    salary_expected: str = Field("", description="Expected salary")
    legally_authorized: bool = Field(False, description="Are you authorized to work in the US?")
    over_18: bool = Field(False, description="Are you over 18 years old?")
    convicted_felony: bool = Field(False, description="Have you been convicted of a felony?")
    felony_explanation: str = Field("", description="If yes, please explain")
    
    # Education
    education: List[Education] = Field(..., description="Education history")
    
    # Employment History
    employment_history: List[EmploymentHistory] = Field(..., description="Employment history")
    
    # References
    references: List[Reference] = Field(..., min_items=3, description="List of references")
    
    # Signature
    signature: str = Field(..., description="Applicant's signature")
    signature_date: str = Field(..., description="Date signed (MM/DD/YYYY)")

class JobApplication(BaseSchema):
    @classmethod
    def get_schema(cls):
        return JobApplicationSchema.schema()

    @classmethod
    def get_name(cls):
        return "job_application"

    @classmethod
    def get_description(cls):
        return "Standard Job Application Form"
