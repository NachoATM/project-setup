from fastapi import APIRouter, Header, Body, HTTPException, UploadFile
from pydantic import BaseModel
from typing import Optional
import uuid
import httpx
import os
from pypdf import PdfMerger

router = APIRouter()
files_database = {}

class CarlemanyFile(BaseModel):
    name : str
    amount_of_pages : int
    path : Optional[str] = None

class Person(BaseModel):
    username : str
    mail : str

class FileObjectDatabase(BaseModel):
    id : str
    owner : Person
    file : CarlemanyFile


async def introspect(auth: str) -> Person:
    url = "http://0.0.0.0:80/introspect"
    headers = {
        "accept": "application/json",
        "auth": auth
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headres=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return Person(**response.json())

class MergeContentInput(BaseModel):
    first_id : str
    second_id : str

@router.post("/merge")
async def files_merge_post(auth: str = Header(alias="auth"), input_body : MergeContentInput = Body()) -> dict[str, str]:

    file_path_1 = files_database.get(input_body.file_id_1)
    file_path_2 = files_database.get(input_body.file_id_2)

    if not file_path_1 or not file_path_2:
        raise HTTPException(status_code=404, detail="One or both file IDs not found")

    merged_id = str(uuid.uuid4())
    merged_name = f"files/{merged_id}.pdf"

    try:
        merger = PdfMerger()
        merger.append(file_path_1)
        merger.append(file_path_2)
        merger.write(merged_name)
        merger.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error merging files: {str(e)}")

    files_database[merged_id] = merged_name

    return {
        "status": "ok",
        "merged_file_id": merged_id
    }

@router.get("")
async def files_get(auth: str = Header(alias="auth")) -> dict[str, str]:
    introspect_response = await introspect(auth=auth)
    print(introspect_response)
    return {"status": "ok"}

@router.post("")
async def files_post(auth: str = Header(alias="auth"), input_body : CarlemanyFile = Body()) -> dict[str, str]:
    current_id = str(uuid.uuid4())
    while current_id in files_database:
        current_id = str(uuid.uuid4())
    introspect_response = await introspect(auth=auth)
    file_object_databse = FileObjectDatabase(
        id = current_id,
        owner = introspect_response,
        file = input_body
    )
    files_database[current_id] = file_object_databse
    return {"file_id": current_id}

# @router.post("/{id}")
# async def files_id_post(id:str, file_content : UploadFile = CarlemanyFile(), auth: str = Header(alias="auth")) -> dict[str, str]:
#     introspect_response = await introspect(auth=auth)
#     if id not in files_database:
#         raise HTTPException(status_code=404, detail="File not found")
#     current_file = files_database[id]
#     if introspect_response.username != current_file.owner.username:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     filename = id + ".pdf"
#     prefix = "files/"

#     with open(prefix + filename, "wb") as buffer:
#        while True:
#         chunk = await file_content.read(8192)
#         if not chunk:
#             break
#         buffer.write(chunk)
#     current_file.file.path = prefix + filename
#     return {"status": "ok"}

from fastapi import Form, File, UploadFile

@router.post("/{id}")
async def files_id_post(
    id: str,
    name: str = Form(...),
    amount_of_pages: int = Form(...),
    file: UploadFile = File(...),
    auth: str = Header(alias="auth")
):
    # Validar token
    introspect_response = await introspect(auth=auth)
    if id not in files_database:
        raise HTTPException(status_code=404, detail="File not found")

    current_file = files_database[id]
    if introspect_response.username != current_file.owner.username:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Guardar fichero en disco
    filename = f"{id}.pdf"
    prefix = "files/"

    with open(prefix + filename, "wb") as buffer:
        while True:
            chunk = await file.read(8192)
            if not chunk:
                break
            buffer.write(chunk)

    # Actualizar en la “base de datos” en memoria
    current_file.file.path = prefix + filename
    current_file.file.name = name
    current_file.file.amount_of_pages = amount_of_pages

    return {
        "status": "ok",
        "message": "File content updated",
        "file_id": id
    }


@router.delete("/{id}")
async def files_id_delete(id:str, auth: str = Header(alias="auth")) -> dict[str, str]:
    introspect_response = await introspect(auth=auth)

    if id not in files_database:
        raise HTTPException(status_code=404, detail="File not found")

    current_file = files_database[id]
    if introspect_response.username != current_file.owner.username:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if current_file.file.path and os.path.exists(current_file.file.path):
        try:
            os.remove(current_file.file.path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

    del files_database[id]

    return {"status": "ok"}

@router.get("/{id}")
async def files_id_get(id: str, auth: str = Header(alias="auth")) -> dict:
    introspect_response = await introspect(auth=auth)

    if id not in files_database:
        raise HTTPException(status_code=404, detail="File not found")

    current_file = files_database[id]

    if introspect_response.username != current_file.owner.username:
        raise HTTPException(status_code=401, detail="Unauthorized")

    file_info = {
        "id": id,
        "name": current_file.file.name,
        "amount_of_pages": current_file.file.amount_of_pages,
        "path": current_file.file.path,
        "owner": {
            "username": current_file.owner.username,
            "mail": current_file.owner.mail
        }
    }

    if current_file.file.path and os.path.exists(current_file.file.path):
        with open(current_file.file.path, "rb") as f:
            file_info["content"] = f.read().hex()

    return {"status": "ok", "file_info": file_info}
