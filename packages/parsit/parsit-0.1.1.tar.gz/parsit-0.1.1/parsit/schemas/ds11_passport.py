from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from enum import Enum
from datetime import date, datetime
from .base import BaseSchema

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    X = "X"  # Undisclosed or another gender identity

class HairColor(str, Enum):
    BALD = "Bald"
    BLACK = "Black"
    BLONDE = "Blonde"
    BROWN = "Brown"
    GRAY = "Gray"
    RED = "Red/Auburn"
    SANDY = "Sandy"
    WHITE = "White"
    OTHER = "Other"

class EyeColor(str, Enum):
    BLACK = "Black"
    BLUE = "Blue"
    BROWN = "Brown"
    GRAY = "Gray"
    GREEN = "Green"
    HAZEL = "Hazel"
    MAROON = "Maroon"
    PINK = "Pink"
    OTHER = "Other"

class PhysicalDescription(BaseModel):
    height_ft: int = Field(..., ge=4, le=8, description="Height in feet")
    height_in: int = Field(..., ge=0, le=11, description="Height in inches")
    hair_color: HairColor = Field(..., description="Hair color")
    eye_color: EyeColor = Field(..., description="Eye color")
    gender: Gender = Field(..., description="Gender")

class AddressHistory(BaseModel):
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State (2-letter code)")
    zip_code: str = Field(..., description="ZIP code")
    country: str = Field("United States", description="Country")
    from_date: str = Field(..., description="From date (MM/YYYY)")
    to_date: str = Field("Present", description="To date (MM/YYYY) or 'Present'")
    current: bool = Field(False, description="Is this your current address?")

class EmergencyContact(BaseModel):
    name: str = Field(..., description="Full name")
    relationship: str = Field(..., description="Relationship to applicant")
    phone_day: str = Field(..., description="Daytime phone number")
    phone_evening: str = Field("", description="Evening phone number")
    email: EmailStr = Field("", description="Email address")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State (2-letter code)")
    zip_code: str = Field(..., description="ZIP code")

class ParentalInfo(BaseModel):
    parent_name: str = Field(..., description="Parent's full name")
    parent_ssn: str = Field("", description="Parent's SSN (last 4 digits)")
    parent_dob: str = Field("", description="Parent's date of birth (MM/DD/YYYY)")
    parent_birth_city: str = Field("", description="Parent's city of birth")
    parent_birth_state: str = Field("", description="Parent's state of birth")
    parent_birth_country: str = Field("", description="Parent's country of birth")

class DS11Schema(BaseModel):
    # Section 1: Type of Application
    application_type: str = Field(..., description="New, Renewal, or Replacement")
    book_type: str = Field(..., description="Book, Card, or Book and Card")
    expedited: bool = Field(False, description="Expedited processing")
    
    # Section 2: Personal Information
    last_name: str = Field(..., description="Last name")
    first_name: str = Field(..., description="First name")
    middle_name: str = Field("", description="Middle name")
    suffix: str = Field("", description="Suffix (Jr., Sr., etc.)")
    has_used_other_names: bool = Field(False, description="Have you used other names?")
    other_names: List[str] = Field([], description="List of other names used")
    
    # Section 3: Date and Place of Birth
    date_of_birth: str = Field(..., description="Date of birth (MM/DD/YYYY)")
    city_of_birth: str = Field(..., description="City of birth")
    state_of_birth: str = Field(..., description="State of birth (if USA)")
    country_of_birth: str = Field(..., description="Country of birth")
    
    # Section 4: Gender
    gender: Gender = Field(..., description="Gender")
    
    # Section 5: Social Security Number
    ssn: str = Field(..., min_length=9, max_length=9, description="Social Security Number")
    
    # Section 6: Contact Information
    day_phone: str = Field(..., description="Daytime phone")
    evening_phone: str = Field("", description="Evening phone")
    email: EmailStr = Field("", description="Email address")
    
    # Section 7: Physical Description
    physical_description: PhysicalDescription = Field(..., description="Physical description")
    
    # Section 8: Address Information
    current_address: AddressHistory = Field(..., description="Current address")
    previous_addresses: List[AddressHistory] = Field([], description="Previous addresses (last 5 years)")
    
    # Section 9: Emergency Contact
    emergency_contact: EmergencyContact = Field(..., description="Emergency contact information")
    
    # Section 10: Parental Information
    mother: ParentalInfo = Field(..., description="Mother's information")
    father: ParentalInfo = Field(..., description="Father's information")
    
    # Section 11: Previous Passport Information
    has_previous_passport: bool = Field(False, description="Have you had a previous U.S. passport?")
    previous_passport_number: str = Field("", description="Previous passport number")
    previous_passport_issue_date: str = Field("", description="Issue date (MM/DD/YYYY)")
    previous_passport_expiry_date: str = Field("", description="Expiry date (MM/DD/YYYY)")
    
    # Section 12: Travel Plans
    travel_plans: str = Field("", description="Travel plans (if any)")
    
    # Section 13: Signature and Date
    signature: str = Field(..., description="Applicant's signature")
    signature_date: str = Field(..., description="Date signed (MM/DD/YYYY)")
    
    # Section 14: Parental Consent (if applicable)
    parental_consent: bool = Field(False, description="Parental consent given (if under 16)")
    parent_signature: str = Field("", description="Parent/guardian signature")
    parent_relationship: str = Field("", description="Relationship to applicant")
    parent_signature_date: str = Field("", description="Date signed (MM/DD/YYYY)")
    
    # Supporting Documents
    birth_certificate_attached: bool = Field(False, description="Birth certificate attached")
    photo_id_attached: bool = Field(False, description="Photo ID attached")
    photo_attached: bool = Field(False, description="Passport photo attached")
    
    @validator('ssn')
    def validate_ssn(cls, v):
        if not v.isdigit() or len(v) != 9:
            raise ValueError('SSN must be 9 digits')
        return v
    
    @validator('date_of_birth', 'previous_passport_issue_date', 'previous_passport_expiry_date', 'signature_date', 'parent_signature_date')
    def validate_date_format(cls, v):
        if v:  # Only validate if the field has a value
            try:
                datetime.strptime(v, '%m/%d/%Y')
            except ValueError:
                raise ValueError('Date must be in MM/DD/YYYY format')
        return v

class DS11Passport(BaseSchema):
    @classmethod
    def get_schema(cls):
        return DS11Schema.schema()

    @classmethod
    def get_name(cls):
        return "ds11_passport"

    @classmethod
    def get_description(cls):
        return "U.S. Passport Application (DS-11)"
