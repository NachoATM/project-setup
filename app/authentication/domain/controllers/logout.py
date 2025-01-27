from fastapi import HTTPException


class LogoutController:
    def __init__(self, token_database: dict):
        self.token_database = token_database
    
    async def __call__(self, auth_token: str):
        if auth_token not in self.token_database:
            raise HTTPException(status_code=401, detail="Unauthorized")
        del self.token_database[auth_token]
        return {"status": "ok"}