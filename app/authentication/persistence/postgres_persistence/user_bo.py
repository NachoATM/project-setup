from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistence.user_bo_interface import UserBOPersistenceServiceInterface 
from app.authentication.domain.persistence.exceptions import UserAlreadyThere 
from app.authentication.models import User

class UserBOPostgresPersistenceService(UserBOPersistenceServiceInterface):

    async def create_user(self, user_bo: UserBO) -> dict:
        if await self.username_exists(username=user_bo.username):
            raise Exception("User already exists")
        new_user = User.create(
            username = user_bo.username,
            hashed_password=user_bo.hashed_password,
            mail=user_bo.mail,
        )
        return user_bo.dict()
    
    async def username_exists(self, username:str) -> bool:
        return (await User.filter(username=username).count()) > 0
    
    async def get(self, username:str) -> UserBO:
        current_user = await User.get(
            username=username
        )
        return UserBO(
            username = current_user.username,
            hashed_password = current_user.hashed_password,
            mail = current_user.mail,
        )