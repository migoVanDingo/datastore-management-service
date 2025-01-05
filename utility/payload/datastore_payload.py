from typing import Optional


class IInsertDatastore:
    name: str
    description: Optional[str] = None
    path: str

class IInsertRoles:
    datastore_id: str
    user_id: str
    role: str
    level: int

class DatastorePayload:

    @staticmethod
    def form_insert_payload(data: dict) -> IInsertDatastore:
        payload = {
            "name": data.get("name"),
            "description": data.get("description"),
            "path": data.get("path")
        }
        return payload
    
    @staticmethod
    def form_insert_roles_payload(data: dict) -> IInsertRoles:
        payload = {
            "datastore_id": data.get("datastore_id"),
            "user_id": data.get("user_id"),
            "role": data.get("role"),
            "level": data.get("level")
        }
        return payload
    