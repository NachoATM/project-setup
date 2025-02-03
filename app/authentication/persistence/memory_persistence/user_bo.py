from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistence.user_bo_interface import UserBOPersistenceServiceInterface 
from app.authentication.domain.persistence.exceptions import UserAlreadyThere 



class UserBOMemoryPersistenceService(UserBOPersistenceServiceInterface):
    def __init__(self):
        self.user_database = {}

    async def create_user(self, user_bo: UserBO) -> dict:
        if user_bo.username in self.user_database:
            raise UserAlreadyThere("User is already there")
        self.user_database[user_bo.username] = user_bo
        return user_bo.dict()
    
    async def username_exists(self, username:str) -> bool:
        return username in self.user_database
    
    async def get(self, username:str) -> UserBO:
        return self.user_database[username]
    
    # def delete(self, username:str):
    #     del self.user_database[username]