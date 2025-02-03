from abc import ABC, abstractmethod


class TokenPersistenceServiceInterface(ABC):
    
    @abstractmethod
    async def create_token(self, username: str) -> str:
        pass
    
    @abstractmethod
    async def delete(self, token:str):
        pass
    
    @abstractmethod
    async def get(self, token:str) -> str:
        pass    