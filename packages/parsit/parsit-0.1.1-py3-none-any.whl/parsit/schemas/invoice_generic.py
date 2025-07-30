from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from .base import BaseSchema

class InvoiceItem(BaseModel):
    description: str = Field(..., description="Item or service description")
    quantity: float = Field(1.0, description="Quantity of items")
    unit_price: float = Field(..., description="Price per unit")
    amount: float = Field(..., description="Total amount (quantity × unit_price)")

class InvoiceSchema(BaseModel):
    invoice_number: str = Field(..., description="Unique invoice number")
    issue_date: str = Field(..., description="Date when invoice was issued (YYYY-MM-DD)")
    due_date: str = Field(..., description="Payment due date (YYYY-MM-DD)")
    
    seller_name: str = Field(..., description="Seller/Company name")
    seller_address: str = Field(..., description="Seller's street address")
    seller_city_state_zip: str = Field(..., description="Seller's city, state, and ZIP code")
    seller_phone: str = Field("", description="Seller's contact phone")
    seller_email: str = Field("", description="Seller's contact email")
    seller_tax_id: str = Field("", description="Seller's tax ID/VAT number")
    
    buyer_name: str = Field(..., description="Buyer/Customer name")
    buyer_address: str = Field("", description="Buyer's street address")
    buyer_city_state_zip: str = Field("", description="Buyer's city, state, and ZIP code")
    
    items: List[InvoiceItem] = Field(..., description="List of items/services")
    subtotal: float = Field(..., description="Subtotal before taxes")
    tax_amount: float = Field(0.0, description="Total tax amount")
    shipping: float = Field(0.0, description="Shipping cost")
    discount: float = Field(0.0, description="Discount amount")
    total: float = Field(..., description="Total amount due")
    
    payment_terms: str = Field("Due on receipt", description="Payment terms")
    payment_instructions: str = Field("", description="Payment instructions")
    notes: str = Field("", description="Additional notes or terms")

class InvoiceGeneric(BaseSchema):
    @classmethod
    def get_schema(cls):
        return InvoiceSchema.schema()

    @classmethod
    def get_name(cls):
        return "generic"

    @classmethod
    def get_description(cls):
        return "Generic invoice schema for standard invoices"
