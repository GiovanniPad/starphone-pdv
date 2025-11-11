from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fullname: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False)
    salary: Decimal = Field(nullable=False)
    hiring_date: datetime = Field(nullable=False)
    resignation_date: datetime = Field(default=None, nullable=True)
    admin: bool = Field(default=False, nullable=False) 
    password: str = Field(nullable=False)

    @property
    def is_admin(self) -> bool:
        return self.admin
