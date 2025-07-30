from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseSchema
from datetime import date

class I9Section1Schema(BaseModel):
    last_name: str = Field(..., description="Employee's last name")
    first_name: str = Field(..., description="Employee's first name")
    middle_initial: str = Field("", description="Middle initial")
    other_names_used: str = Field("", description="Other last names used")
    address: str = Field(..., description="Current address")
    apt_number: str = Field("", description="Apartment number")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    zip_code: str = Field(..., description="ZIP code")
    date_of_birth: str = Field(..., description="Date of birth (MM/DD/YYYY)")
    ssn: str = Field(..., description="Social Security Number")
    email: str = Field("", description="Email address")
    phone: str = Field("", description="Phone number")
    citizenship_status: str = Field(..., description="Citizenship/immigration status")
    alien_number: str = Field("", description="Alien number (if applicable)")
    uscis_number: str = Field("", description="USCIS number (if applicable)")
    foreign_passport: str = Field("", description="Foreign passport information (if applicable)")
    country_of_issuance: str = Field("", description="Country of issuance (if applicable)")
    signature: str = Field(..., description="Employee's signature")
    signature_date: str = Field(..., description="Date signed (MM/DD/YYYY)")
    preparer_name: str = Field("", description="Preparer/translator name (if used)")
    preparer_address: str = Field("", description="Preparer/translator address")
    preparer_signature: str = Field("", description="Preparer/translator signature")
    preparer_date: str = Field("", description="Date prepared (MM/DD/YYYY)")

class I9Section2Schema(BaseModel):
    doc_title: str = Field(..., description="Document title")
    issuing_authority: str = Field(..., description="Issuing authority")
    document_number: str = Field(..., description="Document number")
    expiration_date: str = Field("", description="Expiration date (if any)")
    employer_review_date: str = Field(..., description="Date employer reviewed documents (MM/DD/YYYY)")
    last_name: str = Field(..., description="Employee's last name")
    first_name: str = Field(..., description="Employee's first name")
    employer_name: str = Field(..., description="Employer's business name")
    employer_address: str = Field(..., description="Employer's business address")
    employer_city: str = Field(..., description="Employer's city/state/zip")
    employer_signature: str = Field(..., description="Employer or authorized representative's signature")
    employer_title: str = Field(..., description="Employer's title")
    business_name: str = Field(..., description="Business or organization name")
    business_address: str = Field(..., description="Business or organization address")
    business_city: str = Field(..., description="Business or organization city/state/zip")
    certification_date: str = Field(..., description="Certification date (MM/DD/YYYY)")

class I9(BaseSchema):
    @classmethod
    def get_schema(cls):
        return {
            "section1": I9Section1Schema.schema(),
            "section2": I9Section2Schema.schema()
        }

    @classmethod
    def get_name(cls):
        return "i9"

    @classmethod
    def get_description(cls):
        return "Employment Eligibility Verification (Form I-9)"
