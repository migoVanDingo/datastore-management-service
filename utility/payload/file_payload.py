from typing import Optional
from unicodedata import digit
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
    @staticmethod
    def form_save_file_payload(data) -> ISaveFile:
        payload = {
            "datastore_id": data['datastore_id'],
            "dataset_id": data['dataset_id'],
            "file_name": data['file_name'],
            "file_path": data['file_path'],
            "file_size": data['file_size'],
            "file_type": data['file_type'],
            "create_method": data['create_method'],
            "metadata": data['metadata']
        }
        return payload

    @staticmethod
    def parse_form_data(data) -> ISaveFile:


        payload = {
            "datastore_id": data.get('datastore_id'),
            "dataset_id": data.get('dataset_id'),
            "file_name": data.get('file_name'),
            "file_path": data.get('file_path'),
            "file_size": data.get('file_size'),
            "file_type": data.get('file_type'),
            "create_method": data.get('create_method'),
            "metadata": data.get('metadata')
        }

        return payload
