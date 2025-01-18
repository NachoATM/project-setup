from fastapi import APIRouter, Body, HTTPException, Header
from pydantic import BaseModel
import hashlib
import uuid

router = APIRouter()

user_database = {}
token_database = {}

class RegisterAPIInput(BaseModel):
    username : str
    password : str
    mail : str

@router.post("/register")
async def register(input_body: RegisterAPIInput = Body()) -> dict[str, str]:
    if input_body.username in user_database:
        raise HTTPException(status_code=409, detail="Username already exists")
    hashed_password = hashlib.sha256((input_body.username + input_body.password).encode("utf-8")).hexdigest()
    input_body.password = hashed_password
    user_database[input_body.username] = input_body.dict()
    return input_body.dict()

class LoginAPIInput(BaseModel):
    username : str
    password : str

@router.post("/login")
async def login(input_body: LoginAPIInput = Body()) -> dict[str, str]:
    if not input_body.username in user_database:
        raise HTTPException(status_code=404, detail="Username not found")
    hashed_password = hashlib.sha256((input_body.username + input_body.password).encode("utf-8")).hexdigest()
    if hashed_password != user_database[input_body.username]["password"]:
        raise HTTPException(status_code=401, detail="Password is incorrect")
    current_token = str(uuid.uuid4())
    while current_token in token_database:
        current_token = str(uuid.uuid4())
    token_database[current_token] = input_body.username

    return {"auth": current_token}

@router.get("/introspect")
async def introspect(auth_token: str = Header(alias="auth")) -> dict[str, str]:
    if auth_token not in token_database:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = user_database[token_database[auth_token]].copy()
    del (user["password"])
    return user

@router.post("/logout")
async def logout(auth_token: str = Header(alias="auth")) -> dict[str, str]:
    if auth_token not in token_database:
        raise HTTPException(status_code=401, detail="Unauthorized")
    del token_database[auth_token]
    return {"status": "ok"}
