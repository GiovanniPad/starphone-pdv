from fastapi import APIRouter
from starphone_api.routes.user import router as user_router

main_router = APIRouter()

main_router.include_router(user_router, prefix="/users", tags=["users"])
