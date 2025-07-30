from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date
from .base import BaseSchema
from .registry import SchemaRegistry

class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    amount: float

class InvoiceForm(BaseModel):
    document_type: str = "INVOICE"
    invoice_number: str
    issue_date: date
    due_date: date
    vendor: Dict[str, str]
    customer: Dict[str, str]
    line_items: List[LineItem]
    subtotal: float
    tax: float
    total: float
    payment_terms: str
    notes: Optional[str] = None

@SchemaRegistry.register("INVOICE")
class InvoiceSchema(BaseSchema):
    @classmethod
    def get_schema(cls) -> type[BaseModel]:
        return InvoiceForm
