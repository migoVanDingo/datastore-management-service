from typing import Optional


class IInsertDatastore:
    name: str
    description: Optional[str] = None
    path: str

class DatastorePayload:

    @staticmethod
    def form_insert_payload(name, description, path) -> IInsertDatastore:
        payload = {
            "name": name,
            "description": description,
            "path": path
        }
        return payload
    