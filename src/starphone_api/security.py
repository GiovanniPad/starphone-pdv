from argon2 import PasswordHasher

pwd_context = PasswordHasher()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a hash against a password"""
    return pwd_context.verify(hashed_password, plain_password)


def get_password_hash(password: str) -> str:
    """Generate a hash from plain text"""
    return pwd_context.hash(password)


def check_needs_rehash(hash: str) -> bool:
    return pwd_context.check_needs_rehash(hash)
