from pydantic import BaseModel


class IGetFilesetPath(BaseModel):
    datastore_id: str
    set_id: str
    data_type: str

class PayloadGetFilesetPath:
    @staticmethod
    def form_payload(data: dict) -> IGetFilesetPath:
        return {
            "datastore_id": data.get("datastore_id"),
            "set_id": data.get("set_id"),
            "data_type": data.get("type")
        }