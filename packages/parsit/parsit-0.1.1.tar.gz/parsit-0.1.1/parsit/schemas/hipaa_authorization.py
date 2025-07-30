from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date
from .base import BaseSchema
from .registry import SchemaRegistry

class Recipient(BaseModel):
    name: str = Field(..., description="Recipient's name")
    organization: str = Field("", description="Organization name")
    address: str = Field("", description="Street address")
    city: str = Field("", description="City")
    state: str = Field("", description="State")
    zip_code: str = Field("", description="ZIP code")
    phone: str = Field("", description="Phone number")

class InformationDisclosed(BaseModel):
    medical_records: bool = Field(False, description="Medical records")
    mental_health: bool = Field(False, description="Mental health records")
    hiv_aids: bool = Field(False, description="HIV/AIDS information")
    substance_abuse: bool = Field(False, description="Substance abuse treatment")
    std: bool = Field(False, description="Sexually transmitted diseases")
    genetic_info: bool = Field(False, description="Genetic information")
    other: str = Field("", description="Other specific information")

class HIPAAuthorizationSchema(BaseModel):
    # Patient Information
    patient_name: str = Field(..., description="Patient's full name")
    patient_dob: str = Field(..., description="Date of birth (MM/DD/YYYY)")
    patient_address: str = Field(..., description="Street address")
    patient_city: str = Field(..., description="City")
    patient_state: str = Field(..., description="State")
    patient_zip: str = Field(..., description="ZIP code")
    patient_phone: str = Field(..., description="Phone number")
    patient_email: EmailStr = Field("", description="Email address")
    ssn: str = Field("", description="Social Security Number (last 4 digits)")
    
    # Authorization Details
    purpose: str = Field(..., description="Purpose of the disclosure")
    specific_description: str = Field(..., description="Specific information to be disclosed")
    
    # Information to be Disclosed
    information: InformationDisclosed = Field(..., description="Types of information to disclose")
    
    # Recipient Information
    recipient: Recipient = Field(..., description="Primary recipient of information")
    additional_recipients: List[Recipient] = Field([], description="Additional recipients")
    
    # Expiration
    expiration_date: str = Field("", description="Expiration date (MM/DD/YYYY) or event")
    
    # Patient Rights
    right_to_revoke: bool = Field(True, description="Patient has right to revoke this authorization")
    revocation_instructions: str = Field("", description="Instructions for revocation")
    
    # Signatures
    patient_signature: str = Field(..., description="Patient's signature")
    signature_date: str = Field(..., description="Date signed (MM/DD/YYYY)")
    
    # If signed by personal representative
    representative_name: str = Field("", description="Representative's name (if applicable)")
    representative_relationship: str = Field("", description="Relationship to patient")
    representative_authority: str = Field("", description="Authority to sign")
    
    # Witness (if required)
    witness_name: str = Field("", description="Witness name")
    witness_signature: str = Field("", description="Witness signature")
    witness_date: str = Field("", description="Date witnessed (MM/DD/YYYY)")

@SchemaRegistry.register("hipaa_authorization")
class HIPAAuthorization(BaseSchema):
    @classmethod
    def get_schema(cls):
        return HIPAAuthorizationSchema.schema()

    @classmethod
    def get_name(cls):
        return "hipaa_authorization"

    @classmethod
    def get_description(cls):
        return "HIPAA Authorization Form"
