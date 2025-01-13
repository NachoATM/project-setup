from fastapi import FastAPI
from app.authentication.router import router as router_auth
from app.files.router import router as router_files

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(router_auth, prefix="")
app.include_router(router_files, prefix="/files")

