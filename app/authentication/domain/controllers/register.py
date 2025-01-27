from fastapi import HTTPException

from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistence.exceptions import UserAlreadyThere 
from app.authentication.domain.persistence.user_bo_interface import UserBOPersistenceServiceInterface



class RegisterController:
    def __init__(self, user_database: UserBOPersistenceServiceInterface):
        self.user_database = user_database
    async def __call__(self, user_bo: UserBO):
        try:
            user_bo_dict = await  self.user_database.create_user(user_bo=user_bo)
        except UserAlreadyThere:
            raise HTTPException(status_code=409, detail="Username already exists")

        return user_bo_dict