from typing import Annotated
from sqlmodel import create_engine, Session, SQLModel
from starphone_api.config import settings
from fastapi import Depends

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    connect_args=settings.DATABASE_CONNECT_ARGS,
)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


ActiveSession = Annotated[Session, Depends(get_session)]
