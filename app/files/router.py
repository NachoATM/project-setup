from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def files_get() -> dict[str, str]:
    return {"status": "ok"}

@router.post("")
async def files_post() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/{id}")
async def files_id_get(id:int) -> dict[str, str]:
    return {"status": "ok"}

@router.post("/{id}")
async def files_id_post(id:int) -> dict[str, str]:
    return {"status": "ok"}

@router.delete("/{id}")
async def files_id_delete(id:int) -> dict[str, str]:
    return {"status": "ok"}

@router.post("/merge")
async def files_merge_post() -> dict[str, str]:
    return {"status": "ok"}