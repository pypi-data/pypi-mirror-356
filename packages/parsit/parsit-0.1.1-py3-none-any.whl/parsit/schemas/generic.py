from pydantic import BaseModel, Field
from typing import Dict, Any
from .base import BaseSchema
from .registry import SchemaRegistry

class GenericExtraction(BaseModel):
    extracted_data: Dict[str, Any] = Field(
        ...,
        description="A dictionary of key-value pairs extracted from the document."
    )

@SchemaRegistry.register("GENERIC")
class GenericSchema(BaseSchema):
    @classmethod
    def get_schema(cls) -> type[BaseModel]:
        return GenericExtraction

    @classmethod
    def get_name(cls) -> str:
        return "GENERIC"
