from pydantic import BaseModel


class UserBO(BaseModel):
    username : str
    hashed_password : str
    mail : str