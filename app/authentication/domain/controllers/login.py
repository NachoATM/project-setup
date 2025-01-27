from fastapi import HTTPException
import uuid

from app.authentication.domain.persistence.user_bo_interface import UserBOPersistenceServiceInterface


class LoginController:
    def __init__(self, user_database: UserBOPersistenceServiceInterface, token_database: dict):
        self.user_database = user_database
        self.token_database = token_database


    async def __call__(self, username:str, hashed_password:str) -> str:
        if not await self.user_database.username_exists(username=username):
            raise HTTPException(status_code=404, detail="Username not found")
        current_user = await self.user_database.get(username=username)
        if hashed_password != current_user.hashed_password:
            raise HTTPException(status_code=401, detail="Password is incorrect")
        current_token = str(uuid.uuid4())
        while current_token in self.token_database:
            current_token = str(uuid.uuid4())
        self.token_database[current_token] = username

        return current_token