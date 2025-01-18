from pydantic import BaseModel


class IVerifyFileset(BaseModel):
    datastore_id: str
    set_id: str
    data_type: str




class PayloadVerifyFileset:
    @staticmethod
    def form_payload(data: dict) -> IVerifyFileset:
        return {
            "datastore_id": data.get("datastore_id"),
            "set_id": data.get("set_id"),
            "data_type": data.get("data_type")
        }