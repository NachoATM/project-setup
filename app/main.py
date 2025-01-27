from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
# from app.authentication.router import router as router_auth
from app.authentication.api.router import router as router_auth

from app.files.router import router as router_files
from app.config import DATABASE_URL, models

app = FastAPI()

@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(router_auth, prefix="")
app.include_router(router_files, prefix="/files")

register_tortoise(
    app,
    ob_url=DATABASE_URL,
    modules={"models":models},
    generate_schemas=False,
    add_exception_handlers=True,
)

