from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistence.token_interface import TokenPersistenceServiceInterface 
from app.authentication.domain.persistence.exceptions import UserAlreadyThere 
import uuid
from typing import Union


class TokenMemoryPersistenceService(TokenPersistenceServiceInterface):
    def __init__(self):
        self.token_database = {}

    async def create_token(self, username: str) -> str:
        current_token = str(uuid.uuid4())
        while current_token in self.token_database:
            current_token = str(uuid.uuid4())
        self.token_database[current_token] = username
        return current_token
    
    async def delete(self, token:str):
        del self.token_database[token]
    
    async def get(self, token:str) -> Union[str, None]:
        if token not in self.token_database:
            return None
        return self.token_database[token]
    
    # def delete(self, username:str):
    #     del self.user_database[username]