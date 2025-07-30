from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date
from .base import BaseSchema
from .registry import SchemaRegistry

class Tenant(BaseModel):
    full_name: str = Field(..., description="Tenant's full name")
    phone: str = Field(..., description="Phone number")
    email: EmailStr = Field("", description="Email address")
    ssn: str = Field("", description="Social Security Number (last 4 digits)")
    driver_license: str = Field("", description="Driver's license number and state")
    date_of_birth: str = Field("", description="Date of birth (MM/DD/YYYY)")
    current_address: str = Field("", description="Current address")

class Property(BaseModel):
    address: str = Field(..., description="Full property address")
    unit: str = Field("", description="Unit/apartment number")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    zip_code: str = Field(..., description="ZIP code")
    bedrooms: int = Field(1, description="Number of bedrooms")
    bathrooms: float = Field(1.0, description="Number of bathrooms")
    square_feet: int = Field(0, description="Square footage")
    furnished: bool = Field(False, description="Is the property furnished?")
    parking_spaces: int = Field(0, description="Number of parking spaces")

class Term(BaseModel):
    start_date: str = Field(..., description="Lease start date (MM/DD/YYYY)")
    end_date: str = Field(..., description="Lease end date (MM/DD/YYYY)")
    monthly_rent: float = Field(..., description="Monthly rent amount")
    due_date: int = Field(1, description="Day of month rent is due")
    late_fee: float = Field(0.0, description="Late fee amount")
    grace_period: int = Field(5, description="Grace period in days")
    security_deposit: float = Field(0.0, description="Security deposit amount")
    pet_deposit: float = Field(0.0, description="Pet deposit amount (if applicable)")

class Utilities(BaseModel):
    water_sewer: str = Field("Landlord", description="Responsible party")
    electricity: str = Field("Tenant", description="Responsible party")
    gas: str = Field("Tenant", description="Responsible party")
    trash: str = Field("Landlord", description="Responsible party")
    internet: str = Field("Tenant", description="Responsible party")
    cable: str = Field("Tenant", description="Responsible party")

class LeaseAgreementSchema(BaseModel):
    # Parties
    landlord_name: str = Field(..., description="Landlord's full name")
    landlord_phone: str = Field(..., description="Landlord's phone number")
    landlord_email: EmailStr = Field(..., description="Landlord's email")
    landlord_address: str = Field(..., description="Landlord's mailing address")
    
    tenants: List[Tenant] = Field(..., min_items=1, description="List of all tenants")
    
    # Property Details
    property: Property = Field(..., description="Rental property details")
    
    # Lease Terms
    term: Term = Field(..., description="Lease term details")
    
    # Utilities
    utilities: Utilities = Field(..., description="Utilities responsibility")
    
    # Rules and Policies
    pets_allowed: bool = Field(False, description="Are pets allowed?")
    pet_policy: str = Field("", description="Pet policy details")
    smoking_allowed: bool = Field(False, description="Is smoking allowed?")
    subletting_allowed: bool = Field(False, description="Is subletting allowed?")
    
    # Signatures
    landlord_signature: str = Field(..., description="Landlord's signature")
    landlord_signature_date: str = Field(..., description="Date signed (MM/DD/YYYY)")
    tenant_signatures: List[str] = Field(..., description="Tenants' signatures")
    tenant_signature_dates: List[str] = Field(..., description="Dates signed (MM/DD/YYYY)")
    
    # Additional Terms
    additional_terms: str = Field("", description="Any additional terms or special conditions")

@SchemaRegistry.register("LEASE_AGREEMENT")
class LeaseAgreement(BaseSchema):
    @classmethod
    def get_schema(cls) -> type[BaseModel]:
        return LeaseAgreementSchema

    @classmethod
    def get_name(cls) -> str:
        return "lease_agreement"

    @classmethod
    def get_description(cls) -> str:
        return "Residential Lease Agreement"
