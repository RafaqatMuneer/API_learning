from pydantic import BaseModel, field_validator, model_validator
from typing import Optional

class ProductSchema(BaseModel):
    """ Define how a product look like, define rules and follow those rules exactly
    Rules:
    - id: must be a positive integer
    - name: must be a non-empty string
    - price: must be a positive number
    - in_stock: must be a boolean
    - category: optional string, defaults to "uncategorized"
    """
    id: int
    name: str
    price: float
    in_stock: bool
    category: Optional[str] = "uncategorized"

    @field_validator('id')
    @classmethod
    def id_must_be_positive(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("id must be a positive number")
        return value

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value or value.strip() == '':
            raise ValueError("name cannot be empty")
        return value.strip()

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("price must be greater than 0")
        return value
