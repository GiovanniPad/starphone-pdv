from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field, field_validator

from starphone_api.security import get_password_hash


class UserResponse(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    salary: Decimal
    hiring_date: datetime
    resignation_date: datetime | None = None
    admin: bool
    active: bool

    model_config = {"from_attributes": True}


class UserRequest(BaseModel):
    fullname: str = Field(min_length=1, max_length=255)
    email: EmailStr
    salary: Decimal = Field(gt=Decimal("0"))
    admin: bool = False
    password: str | None = Field(default=None, min_length=8)
    active: bool | None = Field(default=True)

    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return get_password_hash(value)
