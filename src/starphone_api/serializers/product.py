from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class CategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class ProductResponse(BaseModel):
    id: int
    name: str
    category: Optional[CategoryResponse] = None
    quantity: int
    cost_value: Decimal
    profit_value: Decimal

    model_config = {"from_attributes": True}


class ProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    category_id: int = Field(gt=0)
    quantity: int = Field(default=0, ge=0)
    cost_value: Decimal = Field(gt=Decimal("0"))
    profit_value: Decimal = Field(ge=Decimal("0"))

