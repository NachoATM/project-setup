from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistence.token_interface import TokenPersistenceServiceInterface 
from app.authentication.domain.persistence.exceptions import UserAlreadyThere 
import uuid
from typing import Union
from minio import Minio


class FilesMinioPersistenceService(TokenPersistenceServiceInterface):
    def __init__(self):
        self.minio_client = Minio(
            "redis-database:9000",
            access_key="minio",
            secret_key="minio123",
            secure=False,
        )
        self.bucket_name="data-backend-carlemany-s3-bucket"

    def put_file(self, local_path: str, remote_identifier: str):
        self.minio_client.fput_object(
            self.bucket_name,
            object_name=remote_identifier,
            file_path=local_path,
        )
        return "0.0.0.0:9000/" + self.bucket_name + "/" + remote_identifier
    
    def remove_file(self, remote_identifier):
        self.minio_client.remove_object(
            self.bucker_name,
            object_name=remote_identifier,
        )
