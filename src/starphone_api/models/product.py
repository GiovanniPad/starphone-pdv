from decimal import Decimal
from typing import Optional
from sqlmodel import Field, ForeignKey, Relationship, SQLModel

from starphone_api.models.category import Category


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    quantity: int = Field(default=0, nullable=False)
    cost_value: Decimal = Field(nullable=False)
    profit_value: Decimal = Field(nullable=False)

    # Relacionamento com Category
    category: Optional[Category] = Relationship(back_populates="products")
