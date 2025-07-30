from pydantic import BaseModel, Field, constr
from typing import Optional, Literal, List
from datetime import date
from .base import BaseSchema
from .registry import SchemaRegistry

class Address(BaseModel):
    street: Optional[str] = Field(None, description="Street address including apartment or suite number")
    city: Optional[str] = Field(None, description="City or town")
    state_province: Optional[str] = Field(None, description="State or province (if applicable)")
    postal_code: Optional[str] = Field(None, description="ZIP or foreign postal code")
    country: Optional[str] = Field(None, description="Country name (required if different from U.S.)")

class W8BENForm(BaseModel):
    document_type: Literal["W-8BEN"] = "W-8BEN"
    
    # Part I: Identification of Beneficial Owner
    name: Optional[str] = Field(None, description="Name of individual or organization")
    country_of_citizenship: Optional[str] = Field(None, description="Country of citizenship")
    permanent_residence_address: Optional[Address] = Field(None, description="Permanent residence address")
    mailing_address: Optional[Address] = Field(None, description="Mailing address (if different from permanent)")
    
    # Taxpayer Identification Number
    us_tin: Optional[str] = Field(None, description="U.S. taxpayer identification number (if any)")
    foreign_tax_id: Optional[str] = Field(None, description="Foreign tax identifying number")
    foreign_tax_id_country: Optional[str] = Field(None, description="Country that issued the tax ID")
    
    # Part II: Claim of Tax Treaty Benefits
    claim_tax_treaty_benefits: bool = Field(False, description="Check if claiming tax treaty benefits")
    treaty_country: Optional[str] = Field(None, description="Country with which the treaty is claimed")
    treaty_article: Optional[str] = Field(None, description="Article of the treaty")
    treaty_rate: Optional[float] = Field(None, description="Reduced rate of withholding")
    treaty_limitation: Optional[str] = Field(None, description="Type of income covered by treaty")
    
    # Part III: Certification
    beneficial_owner_name: Optional[str] = Field(None, description="Name of beneficial owner")
    beneficial_owner_title: Optional[str] = Field(None, description="Title of signer (if applicable)")
    date_signed: Optional[date] = Field(None, description="Date form was signed")
    
    # Additional Information
    reference_number: Optional[str] = Field(None, description="Reference number (if any)")
    special_rates_conditions: Optional[str] = Field(None, description="Special rates or conditions")

@SchemaRegistry.register("W-8BEN")
class W8BENSchema(BaseSchema):
    @classmethod
    def get_schema(cls) -> type[BaseModel]:
        return W8BENForm
        
    @classmethod
    def get_name(cls) -> str:
        return "w8ben"
        
    @classmethod
    def get_description(cls) -> str:
        return "Certificate of Foreign Status of Beneficial Owner for United States Tax Withholding (Form W-8BEN)"
