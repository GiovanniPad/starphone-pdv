"""ensure_admin_user

Revision ID: 59c771de0067
Revises: 7d43ca224a22
Create Date: 2025-11-12 00:40:01.940324

"""
from datetime import datetime, timezone
from typing import Sequence, Union

from sqlalchemy.exc import IntegrityError

from alembic import op
from sqlmodel import Session, select

from starphone_api.models import User
from starphone_api.security import get_password_hash


# revision identifiers, used by Alembic.
revision: str = "59c771de0067"
down_revision: Union[str, Sequence[str], None] = "7d43ca224a22"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


ADMIN_DEFAULT_PASSWORD = "admin123"
ADMIN_EMAIL = "admin@starphone.com.br"


def upgrade() -> None:
    """Ensure an admin user exists."""
    bind = op.get_bind()
    with Session(bind=bind) as session:
        existing_admin = session.exec(
            select(User).where(User.email == ADMIN_EMAIL)
        ).first()

        if existing_admin:
            return

        now = datetime.now(timezone.utc)
        admin_user = User(
            fullname="Administrador",
            email=ADMIN_EMAIL,
            salary=0,
            hiring_date=now,
            resignation_date=None,
            admin=True,
            password=get_password_hash(ADMIN_DEFAULT_PASSWORD),
            active=True,
        )

        try:
            session.add(admin_user)
            session.commit()
        except IntegrityError:
            session.rollback()

def downgrade() -> None:
    """Remove auto-created admin user."""
    bind = op.get_bind()
    with Session(bind=bind) as session:
        admin_user = session.exec(
            select(User).where(User.email == ADMIN_EMAIL)
        ).first()

        if admin_user:
            session.delete(admin_user)
            session.commit()
