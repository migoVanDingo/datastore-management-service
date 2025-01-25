from pydantic import BaseModel


class IGetDatasetPath(BaseModel):
    dataset_id: str
    datastore_id: str
    directory: str




class PayloadGetDatasetPath:
    @staticmethod
    def form_payload(data: dict) -> IGetDatasetPath:
        return {
            "dataset_id": data.get("dataset_id"),
            "datastore_id": data.get("datastore_id"),
            "directory": data.get("directory")
        }