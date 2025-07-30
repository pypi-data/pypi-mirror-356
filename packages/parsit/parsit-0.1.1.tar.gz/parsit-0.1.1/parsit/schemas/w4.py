from pydantic import BaseModel, Field
from typing import Optional, List
from .base import BaseSchema

class W4Schema(BaseModel):
    employee_first_name: str = Field(..., description="Employee's first name")
    employee_last_name: str = Field(..., description="Employee's last name")
    ssn: str = Field(..., description="Social Security Number")
    address: str = Field(..., description="Home address")
    city_state_zip: str = Field(..., description="City, state, and ZIP code")
    filing_status: str = Field(..., description="Single, Married filing jointly, etc.")
    multiple_jobs: bool = Field(False, description="Multiple jobs or only spouse works")
    dependents_amount: float = Field(0.0, description="Dependents amount")
    other_income: float = Field(0.0, description="Other income amount")
    deductions: float = Field(0.0, description="Deductions amount")
    extra_withholding: float = Field(0.0, description="Extra withholding amount")
    signature: str = Field(..., description="Employee's signature")
    date: str = Field(..., description="Date signed")

class W4(BaseSchema):
    @classmethod
    def get_schema(cls):
        return W4Schema.schema()

    @classmethod
    def get_name(cls):
        return "w4"

    @classmethod
    def get_description(cls):
        return "Employee's Withholding Certificate (Form W-4)"
