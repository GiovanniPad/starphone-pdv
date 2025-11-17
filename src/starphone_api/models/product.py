from decimal import Decimal
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

from starphone_api.models.category import Category
from starphone_api.models.user import User


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    quantity: int = Field(default=0, nullable=False)
    cost_value: Decimal = Field(nullable=False)
    profit_value: Decimal = Field(nullable=False)
    created_by: Optional[int] = Field(foreign_key="user.id", nullable=True, default=None)
    updated_by: Optional[int] = Field(foreign_key="user.id", nullable=True, default=None)

    # Relacionamento com Category
    category: Optional[Category] = Relationship(back_populates="products")
    
    # Relacionamentos com User
    created_by_user: Optional[User] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Product.created_by"}
    )
    updated_by_user: Optional[User] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Product.updated_by"}
    )
