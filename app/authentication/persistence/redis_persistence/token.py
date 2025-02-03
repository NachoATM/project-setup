from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistence.token_interface import TokenPersistenceServiceInterface 
from app.authentication.domain.persistence.exceptions import UserAlreadyThere 
import uuid
from typing import Union
import redis


class TokenRedisPersistenceService(TokenPersistenceServiceInterface):
    def __init__(self):
        self.redis_connection = redis.Redis(
            host="redis-database",
            port="6379",
            decode_responses=True
        )

    async def create_token(self, username: str) -> str:
        current_token = str(uuid.uuid4())
        while self.redis_connection.exists(current_token):
            current_token = str(uuid.uuid4())
        self.redis_connection.set(current_token, username)
        return current_token 
    
    async def delete(self, token:str):
        self.redis_connection.delete(token)
    
    async def get(self, token:str) -> Union[str, None]:
        if not self.redis_connection.exists(token):
            return None
        return self.redis_connection.get(token)