from fastapi import HTTPException
from app.authentication.domain.persistence.token_interface import TokenPersistenceServiceInterface



class LogoutController:
    def __init__(self, token_database: TokenPersistenceServiceInterface):
        self.token_database = token_database
    
    async def __call__(self, auth_token: str):
        username = self.token_database.get(token=auth_token)
        if username is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        await self.token_database.delete(token=auth_token)