from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from starphone_api.auth import get_current_user
from starphone_api.db import ActiveSession
from starphone_api.models import Category
from starphone_api.serializers.product import CategoryRequest, CategoryResponse

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=CategoryResponse)
async def create_category(*, session: ActiveSession, category: CategoryRequest):
    # Verificar se já existe uma categoria com o mesmo nome
    existing = session.exec(select(Category).where(Category.name == category.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Categoria com este nome já existe")
    
    db_category = Category(name=category.name)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return CategoryResponse.model_validate(db_category)


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(*, session: ActiveSession):
    categories = session.exec(select(Category)).all()
    return [CategoryResponse.model_validate(category) for category in categories]


@router.get("/{category_id}/", response_model=CategoryResponse)
async def get_category(*, session: ActiveSession, category_id: int):
    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return CategoryResponse.model_validate(category)


@router.put("/{category_id}/", response_model=CategoryResponse)
async def update_category(*, session: ActiveSession, category_id: int, category: CategoryRequest):
    db_category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    # Verificar se já existe outra categoria com o mesmo nome
    existing = session.exec(
        select(Category).where(Category.name == category.name, Category.id != category_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Categoria com este nome já existe")
    
    db_category.name = category.name
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return CategoryResponse.model_validate(db_category)


@router.delete("/{category_id}/", response_model=CategoryResponse)
async def delete_category(*, session: ActiveSession, category_id: int):
    category = session.exec(select(Category).where(Category.id == category_id)).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    # Verificar se há produtos associados a esta categoria
    from starphone_api.models import Product
    products = session.exec(select(Product).where(Product.category_id == category_id)).all()
    if products:
        count = len(products)
        raise HTTPException(
            status_code=400,
            detail=f"Não é possível excluir categoria com {count} produto(s) associado(s). Remova os produtos antes de excluir a categoria."
        )
    
    session.delete(category)
    session.commit()
    return CategoryResponse.model_validate(category)

