from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select

from starphone_api.auth import get_current_user
from starphone_api.db import ActiveSession
from starphone_api.models import Category, Product, User
from starphone_api.serializers.product import ProductRequest, ProductResponse

router = APIRouter()


@router.post("/", response_model=ProductResponse)
async def create_product(
    *,
    session: ActiveSession,
    product: ProductRequest,
    current_user: User = Depends(get_current_user),  # Obtém o usuário do token JWT
):
    # Verificar se a categoria existe
    category = session.exec(select(Category).where(Category.id == product.category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    # Criar produto com os dados do usuário autenticado obtido do token JWT
    db_product = Product(
        name=product.name,
        category_id=product.category_id,
        quantity=product.quantity,
        cost_value=product.cost_value,
        profit_value=product.profit_value,
        created_by=current_user.id,  # ID do usuário obtido do token JWT
        updated_by=current_user.id,  # ID do usuário obtido do token JWT
    )
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    
    # Carregar relacionamentos
    stmt = (
        select(Product)
        .where(Product.id == db_product.id)
        .options(
            selectinload(Product.category),
            selectinload(Product.created_by_user),
            selectinload(Product.updated_by_user),
        )
    )
    db_product = session.exec(stmt).first()
    
    return ProductResponse.model_validate(db_product)


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    *,
    session: ActiveSession,
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Product)
        .options(
            selectinload(Product.category),
            selectinload(Product.created_by_user),
            selectinload(Product.updated_by_user),
        )
    )
    products = session.exec(stmt).all()
    return [ProductResponse.model_validate(product) for product in products]


@router.get("/{product_id}/", response_model=ProductResponse)
async def get_product(
    *,
    session: ActiveSession,
    product_id: int,
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Product)
        .where(Product.id == product_id)
        .options(
            selectinload(Product.category),
            selectinload(Product.created_by_user),
            selectinload(Product.updated_by_user),
        )
    )
    product = session.exec(stmt).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return ProductResponse.model_validate(product)


@router.put("/{product_id}/", response_model=ProductResponse)
async def update_product(
    *,
    session: ActiveSession,
    product_id: int,
    product: ProductRequest,
    current_user: User = Depends(get_current_user),  # Obtém o usuário do token JWT
):
    db_product = session.exec(select(Product).where(Product.id == product_id)).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Verificar se a categoria existe
    category = session.exec(select(Category).where(Category.id == product.category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    # Atualizar produto com os dados do usuário autenticado obtido do token JWT
    db_product.name = product.name
    db_product.category_id = product.category_id
    db_product.quantity = product.quantity
    db_product.cost_value = product.cost_value
    db_product.profit_value = product.profit_value
    db_product.updated_by = current_user.id  # ID do usuário obtido do token JWT
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    
    # Carregar relacionamentos
    stmt = (
        select(Product)
        .where(Product.id == db_product.id)
        .options(
            selectinload(Product.category),
            selectinload(Product.created_by_user),
            selectinload(Product.updated_by_user),
        )
    )
    db_product = session.exec(stmt).first()
    
    return ProductResponse.model_validate(db_product)


@router.delete("/{product_id}/", response_model=ProductResponse)
async def delete_product(
    *,
    session: ActiveSession,
    product_id: int,
    current_user: User = Depends(get_current_user),
):
    # Carregar o produto com todos os relacionamentos usando selectinload
    stmt = (
        select(Product)
        .where(Product.id == product_id)
        .options(
            selectinload(Product.category),
            selectinload(Product.created_by_user),
            selectinload(Product.updated_by_user),
        )
    )
    product = session.exec(stmt).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Criar uma cópia dos dados para o response antes de deletar
    response_data = ProductResponse.model_validate(product)
    
    session.delete(product)
    session.commit()
    return response_data

