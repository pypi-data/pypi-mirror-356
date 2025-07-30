from pydantic import BaseModel, Field
from typing import List, Optional
from .base import BaseSchema

class Form1040Schema(BaseModel):
    filing_status: str = Field(..., description="Filing status (e.g., Single, Married Filing Jointly)")
    first_name: str = Field(..., description="Taxpayer's first name")
    last_name: str = Field(..., description="Taxpayer's last name")
    ssn: str = Field(..., description="Social Security Number")
    address: str = Field(..., description="Street address")
    city_state_zip: str = Field(..., description="City, state, and ZIP code")
    wages: float = Field(..., description="Wages, salaries, tips, etc.")
    taxable_interest: float = Field(0.0, description="Taxable interest")
    ordinary_dividends: float = Field(0.0, description="Ordinary dividends")
    ira_deduction: float = Field(0.0, description="IRA deduction")
    taxable_income: float = Field(..., description="Taxable income")
    federal_income_tax_withheld: float = Field(0.0, description="Federal income tax withheld")
    refund_amount: float = Field(0.0, description="Amount to be refunded")
    amount_you_owe: float = Field(0.0, description="Amount you owe")
    signature: str = Field(..., description="Taxpayer's signature")
    date: str = Field(..., description="Date signed")

class Form1040(BaseSchema):
    @classmethod
    def get_schema(cls):
        return Form1040Schema.schema()

    @classmethod
    def get_name(cls):
        return "form_1040"

    @classmethod
    def get_description(cls):
        return "U.S. Individual Income Tax Return (Form 1040)"
