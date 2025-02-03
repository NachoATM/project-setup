from fastapi import HTTPException

from app.authentication.domain.persistence.user_bo_interface import UserBOPersistenceServiceInterface
from app.authentication.domain.persistence.token_interface import TokenPersistenceServiceInterface


class IntrospectController:
    def __init__(self, user_database: UserBOPersistenceServiceInterface, token_database: TokenPersistenceServiceInterface):
        self.user_database = user_database
        self.token_database = token_database

    async def __call__(self, auth_token: str) -> dict:
        username = await self.token_database.get(token=auth_token)
        if auth_token is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        user_bo = await self.user_database.get(username=username)
        current_user = user_bo .dict()

        del (current_user["hashed_password"])
        return current_user