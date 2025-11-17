from decimal import Decimal
from typing import Optional, Any

from pydantic import BaseModel, Field, model_validator


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class CategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class UserInfoResponse(BaseModel):
    name: str
    email: str

    model_config = {"from_attributes": True}


class ProductResponse(BaseModel):
    id: int
    name: str
    category: Optional[CategoryResponse] = None
    quantity: int
    cost_value: Decimal
    profit_value: Decimal
    created_by: Optional[UserInfoResponse] = None
    updated_by: Optional[UserInfoResponse] = None

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def transform_user_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return data
        
        # Se for um objeto do modelo Product
        if hasattr(data, "created_by_user") and hasattr(data, "updated_by_user"):
            result = {
                "id": data.id,
                "name": data.name,
                "category": data.category,
                "quantity": data.quantity,
                "cost_value": data.cost_value,
                "profit_value": data.profit_value,
            }
            
            # Transformar created_by_user em created_by
            if data.created_by_user:
                result["created_by"] = {
                    "name": data.created_by_user.fullname,
                    "email": data.created_by_user.email,
                }
            
            # Transformar updated_by_user em updated_by
            if data.updated_by_user:
                result["updated_by"] = {
                    "name": data.updated_by_user.fullname,
                    "email": data.updated_by_user.email,
                }
            
            return result
        
        return data


class ProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    category_id: int = Field(gt=0)
    quantity: int = Field(default=0, ge=0)
    cost_value: Decimal = Field(gt=Decimal("0"))
    profit_value: Decimal = Field(ge=Decimal("0"))

