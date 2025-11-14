from fastapi import APIRouter
from starphone_api.routes.category import router as category_router
from starphone_api.routes.product import router as product_router
from starphone_api.routes.user import router as user_router

main_router = APIRouter()

main_router.include_router(user_router, prefix="/users", tags=["users"])
main_router.include_router(product_router, prefix="/products", tags=["products"])
main_router.include_router(category_router, prefix="/categories", tags=["categories"])
