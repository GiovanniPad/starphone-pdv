from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from starphone_api.db import ActiveSession
from starphone_api.models import User
from starphone_api.serializers.user import UserRequest, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(*, session: ActiveSession, user: UserRequest):
    hiring_date = datetime.now(timezone.utc)
    if user.password is None:
        raise HTTPException(
            status_code=400,
            detail="Senha é obrigatória para criação de usuário",
        )
    user = User(
        fullname=user.fullname,
        email=user.email,
        salary=user.salary,
        hiring_date=hiring_date,
        admin=user.admin,
        password=user.password,
        active=user.active if user.active is not None else True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse.model_validate(user)


@router.get("/", response_model=list[UserResponse])
async def get_users(*, session: ActiveSession):
    users = session.exec(select(User)).all()
    return [UserResponse.model_validate(user) for user in users]


@router.get("/{email}/", response_model=UserResponse)
async def get_user_by_email(*, session: ActiveSession, email: str):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return UserResponse.model_validate(user)


@router.put("/{email}/", response_model=UserResponse)
async def update_user(*, session: ActiveSession, email: str, user: UserRequest):
    db_user = session.exec(select(User).where(User.email == email)).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    # hiring_date é imutável após criação
    db_user.fullname = user.fullname
    db_user.email = user.email
    db_user.salary = user.salary
    db_user.admin = user.admin
    if user.password:
        db_user.password = user.password

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return UserResponse.model_validate(db_user)


@router.delete("/{email}/", response_model=UserResponse)
async def delete_user(*, session: ActiveSession, email: str):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user.resignation_date = datetime.now(timezone.utc)
    user.active = False
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse.model_validate(user)
