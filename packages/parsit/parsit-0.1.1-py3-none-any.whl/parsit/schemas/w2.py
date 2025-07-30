from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseSchema

class W2Schema(BaseModel):
    employer_name: str = Field(..., description="Employer's name")
    employer_ein: str = Field(..., description="Employer's EIN")
    employer_address: str = Field(..., description="Employer's street address")
    employer_city_state_zip: str = Field(..., description="Employer's city, state, and ZIP code")
    employee_ssn: str = Field(..., description="Employee's Social Security Number")
    employee_name: str = Field(..., description="Employee's name")
    employee_address: str = Field(..., description="Employee's street address")
    employee_city_state_zip: str = Field(..., description="Employee's city, state, and ZIP code")
    control_number: str = Field("", description="Control number (if any)")
    wages_tips_other_comp: float = Field(..., description="Wages, tips, other compensation")
    federal_income_tax_withheld: float = Field(..., description="Federal income tax withheld")
    social_security_wages: float = Field(..., description="Social security wages")
    social_security_tax_withheld: float = Field(..., description="Social security tax withheld")
    medicare_wages: float = Field(..., description="Medicare wages and tips")
    medicare_tax_withheld: float = Field(..., description="Medicare tax withheld")
    social_security_tips: float = Field(0.0, description="Social security tips")
    allocated_tips: float = Field(0.0, description="Allocated tips")
    dependent_care_benefits: float = Field(0.0, description="Dependent care benefits")
    nonqualified_plans: float = Field(0.0, description="Nonqualified plans")

class W2(BaseSchema):
    @classmethod
    def get_schema(cls):
        return W2Schema.schema()

    @classmethod
    def get_name(cls):
        return "w2"

    @classmethod
    def get_description(cls):
        return "Wage and Tax Statement (Form W-2)"
