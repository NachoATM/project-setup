from abc import ABC, abstractmethod

from app.authentication.domain.bo.user_bo import UserBO


class UserBOPersistenceServiceInterface(ABC):
    
    @abstractmethod
    async def create_user(self, user_bo: UserBO) -> dict:
       pass
    
    @abstractmethod
    async def username_exists(self, username:str) -> bool:
        pass
    
    @abstractmethod
    async def get(self, username:str) -> UserBO:
        pass