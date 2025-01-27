from fastapi import HTTPException

from app.authentication.domain.persistence.user_bo_interface import UserBOPersistenceServiceInterface


class IntrospectController:
    def __init__(self, user_database: UserBOPersistenceServiceInterface, token_database: dict):
        self.user_database = user_database
        self.token_database = token_database

    async def __call__(self, auth_token: str) -> dict:
        if auth_token not in self.token_database:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        user_bo = await self.user_database.get(username=self.token_database[auth_token])
        current_user = user_bo .dict()

        del (current_user["hashed_password"])
        return current_user