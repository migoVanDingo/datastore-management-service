from typing import Optional
from pydantic import BaseModel


class IInsertDataset(BaseModel):
    name: str
    description: Optional[str]
    path: str
    datastore_id: str

class IInsertDatasetRoles(BaseModel):
    dataset_id: str
    user_id: str
    role: str
    level: int

class DatasetPayload:

    @staticmethod
    def form_dataset_insert_payload(data: dict) -> IInsertDataset:
        payload = {
            "name": data.get("name"),
            "description": data.get("description"),
            "path": data.get("path"),
            "datastore_id": data.get("datastore_id")
        }
        return payload
    
    @staticmethod
    def form_dataset_roles_insert_payload(data: dict) -> IInsertDatasetRoles:
        payload = {
            "dataset_id": data.get("dataset_id"),
            "user_id": data.get("user_id"),
            "role": data.get("role"),
            "level": data.get("level")
        }
        return payload