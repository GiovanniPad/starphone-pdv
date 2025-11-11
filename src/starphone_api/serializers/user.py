import datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator, ValidationInfo, Field, model_validator


class UserRequest(BaseModel):
    fullname: str = Field(..., min_length=3, max_length=100)
    email: str = Field(..., format="email")
    salary: Decimal = Field(..., gt=0)
    hiring_date: datetime = Field(..., format="date")
    resignation_date: datetime | None = Field(default=None, format="date")
    admin: bool = Field(default=False)
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator("email")
    def validate_email(self, value: str) -> str:
        return value.lower()