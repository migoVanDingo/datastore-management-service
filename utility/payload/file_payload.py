from typing import Optional
from unicodedata import digit
from flask import json
from pydantic import BaseModel


class ISaveFile(BaseModel):
    datastore_id: str
    dataset_id: Optional[str] = None
    file_name: str
    file_path: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    create_method: Optional[str] = None
    metadata: Optional[str] = None


class FilePayload:
    # @staticmethod
    # def form_save_file_payload(data) -> ISaveFile:
    #     payload = {
    #         "datastore_id": data['datastore_id'],
    #         "dataset_id": data['dataset_id'],
    #         "file_name": data['file_name'],
    #         "file_path": data['file_path'],
    #         "file_size": data['file_size'],
    #         "file_type": data['file_type'],
    #         "create_method": data['create_method'],
    #         "metadata": data['metadata']
    #     }
    #     return payload

    @staticmethod
    def form_save_file_payload(data) -> ISaveFile:


        payload = {
            "datastore_id": data.get('datastore_id'),
            "dataset_id": data.get('dataset_id'),
            "file_name": data.get('file_name'),
            "file_path": data.get('file_path'),
            "file_size": data.get('size'),
            "file_type": data.get('file_type'),
            "create_method": data.get('create_method'),
            "created_by": data.get('user_id'),
            "metadata": json.dumps({
                "tags": data.get('tags'),
                "size": data.get('size'),
                "type": data.get('type')
            }) 
        }

        return payload
    

    @staticmethod
    def form_insert_datastore_file_payload(data) -> dict:
        payload = {
            "datastore_id": data.get('datastore_id'),
            "file_id": data.get('file_id'),
            "created_by": data.get('created_by'),
        }
        return payload
