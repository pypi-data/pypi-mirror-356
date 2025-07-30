from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseSchema

class W9Schema(BaseModel):
    name: str = Field(..., description="Name as shown on your income tax return")
    business_name: str = Field("", description="Business name/disregarded entity name (if different from above)")
    federal_tax_classification: str = Field(..., description="Federal tax classification")
    exemptions: str = Field("", description="Exemptions (if any)")
    address: str = Field(..., description="Address (number, street, and apt or suite no.)")
    city_state_zip: str = Field(..., description="City, state, and ZIP code")
    account_numbers: str = Field("", description="List account number(s) (optional)")
    requester_name: str = Field("", description="Requester's name and address (optional)")
    ssn_or_tin: str = Field(..., description="Social Security number or employer identification number")
    date: str = Field(..., description="Date (MM/DD/YYYY)")
    signature: str = Field(..., description="Signature")

class W9(BaseSchema):
    @classmethod
    def get_schema(cls):
        return W9Schema.schema()

    @classmethod
    def get_name(cls):
        return "w9"

    @classmethod
    def get_description(cls):
        return "Request for Taxpayer Identification Number and Certification (Form W-9)"
