from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from starphone_api.db import ActiveSession
from starphone_api.models import User

router = APIRouter()


@router.post("/", response_model=User)
async def create_user(*, session: ActiveSession, user: User):
    user = User(
        fullname=user.fullname,
        email=user.email,
        salary=user.salary,
        hiring_date=user.hiring_date,
        resignation_date=user.resignation_date,
        admin=user.admin,
        password=user.password,
    )
    session.add(user)
    session.commit()
    return user


@router.get("/", response_model=User)
async def get_users(*, session: ActiveSession):
    users = session.exec(select(User)).all()
    return users


@router.get("/{email}/", response_model=User)
async def get_user_by_email(*, session: ActiveSession, email: str):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{email}/", response_model=User)
async def update_user(*, session: ActiveSession, email: str, user: User):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.fullname = user.fullname
    user.email = user.email
    user.salary = user.salary
    user.hiring_date = user.hiring_date
    user.resignation_date = user.resignation_date
    user.admin = user.admin
    user.password = user.password

    session.add(user)
    session.commit()
    return user


@router.delete("/{email}/", response_model=User)
async def delete_user(*, session: ActiveSession, email: str):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.resignation_date = datetime.now(timezone.utc)
    session.add(user)
    session.commit()
    return user