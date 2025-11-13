from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, ForeignKey, Relationship, SQLModel

from starphone_api.models.category import Category

if TYPE_CHECKING:
    from starphone_api.models.user import User


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    quantity: int = Field(default=0, nullable=False)
    cost_value: Decimal = Field(nullable=False)
    profit_value: Decimal = Field(nullable=False)
    created_by_id: int = Field(foreign_key="user.id", nullable=False)
    updated_by_id: Optional[int] = Field(foreign_key="user.id", default=None, nullable=True)

    # Relacionamento com Category
    category: Optional[Category] = Relationship(back_populates="products")

    # Relacionamentos com User
    created_by: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Product.created_by_id"}
    )
    updated_by: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Product.updated_by_id"}
    )
