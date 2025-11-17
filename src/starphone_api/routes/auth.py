from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from starphone_api.auth import get_current_user, login_for_access_token
from starphone_api.db import ActiveSession
from starphone_api.models import User
from starphone_api.serializers.auth import TokenResponse
from starphone_api.serializers.user import UserResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
    session: ActiveSession,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Autentica um usuário e retorna um token JWT.
    Segue o padrão OAuth2 recomendado pela documentação do FastAPI.
    
    Args:
        form_data: Formulário OAuth2 com username (email) e password
        session: Sessão do banco de dados
    
    Returns:
        Token JWT e tipo de token
    
    Raises:
        HTTPException: Se as credenciais forem inválidas
    """
    # OAuth2PasswordRequestForm usa "username" para o email
    return await login_for_access_token(
        email=form_data.username,
        password=form_data.password,
        session=session,
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Retorna as informações do usuário autenticado.
    
    Args:
        current_user: Usuário autenticado (obtido via dependência)
    
    Returns:
        Informações do usuário
    """
    return UserResponse.model_validate(current_user)

