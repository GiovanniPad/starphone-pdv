from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select

from starphone_api.auth import get_current_user
from starphone_api.db import ActiveSession
from starphone_api.models import Category, Product
from starphone_api.serializers.product import ProductRequest, ProductResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=ProductResponse)
async def create_product(*, session: ActiveSession, product: ProductRequest):
    # Verificar se a categoria existe
    category = session.exec(select(Category).where(Category.id == product.category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    db_product = Product(
        name=product.name,
        category_id=product.category_id,
        quantity=product.quantity,
        cost_value=product.cost_value,
        profit_value=product.profit_value,
    )
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return ProductResponse.model_validate(db_product)


@router.get("/", response_model=list[ProductResponse])
async def get_products(*, session: ActiveSession):
    products = session.exec(select(Product)).all()
    return [ProductResponse.model_validate(product) for product in products]


@router.get("/{product_id}/", response_model=ProductResponse)
async def get_product(*, session: ActiveSession, product_id: int):
    product = session.exec(select(Product).where(Product.id == product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return ProductResponse.model_validate(product)


@router.put("/{product_id}/", response_model=ProductResponse)
async def update_product(*, session: ActiveSession, product_id: int, product: ProductRequest):
    db_product = session.exec(select(Product).where(Product.id == product_id)).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Verificar se a categoria existe
    category = session.exec(select(Category).where(Category.id == product.category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    db_product.name = product.name
    db_product.category_id = product.category_id
    db_product.quantity = product.quantity
    db_product.cost_value = product.cost_value
    db_product.profit_value = product.profit_value
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return ProductResponse.model_validate(db_product)


@router.delete("/{product_id}/", response_model=ProductResponse)
async def delete_product(*, session: ActiveSession, product_id: int):
    # Carregar o produto com o relacionamento category usando selectinload
    stmt = select(Product).where(Product.id == product_id).options(selectinload(Product.category))
    product = session.exec(stmt).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Criar uma cópia dos dados para o response antes de deletar
    response_data = ProductResponse.model_validate(product)
    
    session.delete(product)
    session.commit()
    return response_data

