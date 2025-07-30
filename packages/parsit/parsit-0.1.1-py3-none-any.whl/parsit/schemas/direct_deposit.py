from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from .base import BaseSchema

class DirectDepositSchema(BaseModel):
    # Employee Information
    employee_name: str = Field(..., description="Employee's full name")
    employee_id: str = Field(..., description="Employee ID")
    ssn: str = Field("", description="Last 4 digits of SSN")
    department: str = Field("", description="Department name")
    position: str = Field("", description="Job title/position")
    
    # Bank Account Information
    account_holder_name: str = Field(..., description="Name on the bank account")
    bank_name: str = Field(..., description="Name of financial institution")
    bank_address: str = Field(..., description="Bank's street address")
    bank_city: str = Field(..., description="Bank's city")
    bank_state: str = Field(..., description="Bank's state")
    bank_zip: str = Field(..., description="Bank's ZIP code")
    routing_number: str = Field(..., min_length=9, max_length=9, description="ABA/Routing number (9 digits)")
    account_number: str = Field(..., description="Bank account number")
    account_type: str = Field(..., description="Checking or Savings")
    
    # Deposit Details
    deposit_type: str = Field("Full", description="Full amount or partial amount")
    deposit_amount: Optional[float] = Field(None, description="Amount if partial deposit")
    remaining_amount_account: Optional[str] = Field("", description="Account for remaining amount if partial")
    
    # Authorization
    signature: str = Field(..., description="Employee's signature")
    signature_date: str = Field(..., description="Date signed (MM/DD/YYYY)")
    
    # Employer Section
    employer_name: str = Field("", description="Employer's name")
    employer_authorized_by: str = Field("", description="Authorized by (print name)")
    employer_signature: str = Field("", description="Authorized signature")
    employer_date: str = Field("", description="Date authorized (MM/DD/YYYY)")
    
    # Verification
    voided_check_attached: bool = Field(False, description="Voided check attached")
    bank_letter_attached: bool = Field(False, description="Bank letter attached")
    
    @validator('routing_number')
    def validate_routing_number(cls, v):
        if not v.isdigit() or len(v) != 9:
            raise ValueError('Routing number must be 9 digits')
        return v
    
    @validator('account_type')
    def validate_account_type(cls, v):
        if v.lower() not in ['checking', 'savings']:
            raise ValueError('Account type must be either Checking or Savings')
        return v.lower()

class DirectDeposit(BaseSchema):
    @classmethod
    def get_schema(cls):
        return DirectDepositSchema.schema()

    @classmethod
    def get_name(cls):
        return "direct_deposit"

    @classmethod
    def get_description(cls):
        return "Direct Deposit Authorization Form"
