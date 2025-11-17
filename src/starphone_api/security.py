from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

pwd_context = PasswordHasher()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def check_needs_rehash(hash: str) -> bool:
    return pwd_context.check_needs_rehash(hash)
