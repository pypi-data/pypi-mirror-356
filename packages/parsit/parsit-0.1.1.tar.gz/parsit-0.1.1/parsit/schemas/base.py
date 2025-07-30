from pydantic import BaseModel
from typing import Type

class BaseSchema:
    @classmethod
    def get_schema(cls) -> Type[BaseModel]:
        raise NotImplementedError("Subclasses must implement get_schema()")
