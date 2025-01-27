from fastapi import APIRouter, Body, HTTPException, Header
from pydantic import BaseModel
import hashlib
import uuid
# import typing import Union -- No sé si es necesaria esta lib

token_database_dict = {} #tiene que ir aqui por que se usa para las import e las form app

from app.authentication.domain.bo.user_bo import UserBO

# from app.authentication.domain.controllers.register import RegisterController

# # from app.authentication.domain.controllers.login import LoginController
# # from app.authentication.domain.controllers.introspect import IntrospectController

# from app.authentication.domain.controllers.logout import LogoutController
from app.authentication.persistence.memory_persistence.user_bo import UserBOPersistenceService


from app.authentication.dependency_injection.domain.introspect import IntrospectControllers
from app.authentication.dependency_injection.domain.login import LoginControllers
from app.authentication.dependency_injection.domain.register import RegisterControllers
from app.authentication.dependency_injection.domain.logout import LogoutControllers



router = APIRouter()

user_database_dict = {}


user_database = UserBOPersistenceService(user_database_dict=user_database_dict)

register_controller = RegisterControllers.carlemany()
login_controller = LoginControllers.carlemany()
introspect_controller = IntrospectControllers.carlemany()
logout_controller = LogoutControllers.carlemany()


class RegisterAPIInput(BaseModel):
    username : str
    password : str
    mail : str

@router.post("/register")
async def register(input_body: RegisterAPIInput = Body()) -> dict[str, str]:
    hashed_password = hashlib.sha256((input_body.username + input_body.password).encode("utf-8")).hexdigest()
    input_body.password = hashed_password

    user_bo = UserBO(
        username=input_body.username,
        password=hashed_password,
        mail=input_body.mail,
    )
    output = await register_controller(user_bo=user_bo)
    return output

class LoginAPIInput(BaseModel):
    username : str
    password : str

@router.post("/login")
async def login(input_body: LoginAPIInput = Body()) -> dict[str, str]:
    
    hashed_password = hashlib.sha256((input_body.username + input_body.password).encode("utf-8")).hexdigest()
    input_body.password = hashed_password

    current_token = await login_controller(username=input_body.username, hashed_password=input_body.password)

    return {"auth": current_token}

@router.get("/introspect")
async def introspect(auth_token: str = Header(alias="auth")) -> dict[str, str]:
    
    user_dict = await introspect_controller(auth_token=auth_token)
    
    return user_dict

@router.post("/logout")
async def logout(auth_token: str = Header(alias="auth")) -> dict[str, str]:
    await logout_controller(auth_token=auth_token)
    return {"status": "ok"}
