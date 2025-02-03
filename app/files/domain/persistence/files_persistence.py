from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistence.token_interface import TokenPersistenceServiceInterface 
from app.authentication.domain.persistence.exceptions import UserAlreadyThere 
import uuid
from typing import Union
from minio import Minio
from abc import ABC, abstractmethod


class FilesPersistenceServiceInterface(ABC):

    @abstractmethod
    async def put_file(self, local_path: str, remote_identifier: str):
       pass

    @abstractmethod
    async def remove_file(self, remote_identifier):
       pass