from fastapi import HTTPException, status

from app.auth import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas import Token


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def login(self, username: str, password: str) -> Token:
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        token = create_access_token({"sub": user.username})
        return Token(access_token=token)
