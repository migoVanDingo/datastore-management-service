import traceback

from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError
from utility.payload.dataset_payload import DatasetPayload
from utility.request import Request


class RequestAddFileToDataset(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- RequestAddFileToDatasetPayload: {self.payload}")

            # Parse Payload for datasetId, userId
            dataset_id = self.payload.get("dataset_id")
            user_id = self.payload.get("user_id")

            if not dataset_id or not user_id:
                return {"error": "Missing dataset_id or user_id in payload"}
            
            if not self.payload.get("files") or len(self.payload.get("files")) == 0:
                return {"error": "No files to add to dataset"}
            
            dao_request = Request()
            datastore = dao_request.read(self.request_id, "dataset", {"dataset_id": dataset_id})

            datastore_id = datastore["response"]["datastore_id"]

            response_arr = []

            # Loop through payload files
            for file in self.payload.get("files"):
                set_id = file.get("set_id")
                file_type = file.get("type")

                query = f"SELECT file_id FROM files WHERE datastore_id = '{datastore_id}' AND file_type = '{file_type}' AND JSON_EXTRACT(metadata, '$.set_id') = '{set_id}'"


                # -> Use set_id to get all files from files table with the same set_id
                file_set = dao_request.query(self.request_id, query)   
                file_set = file_set["response"]

                current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- File Set: {file_set}")

                for insert_file in file_set:
                    # -> Insert file into dataset_files table
                    dataset_file_payload = {
                        "dataset_id": dataset_id,
                        "file_id": insert_file["file_id"],
                        "user_id": user_id,
                        "set_id": set_id,
                        "file_type": file_type

                    }
                    insert_response = dao_request.insert(self.request_id, "dataset_files", DatasetPayload.form_dataset_files_insert_payload(dataset_file_payload))

                    response_arr.append(insert_response["response"])


                
            length = len(response_arr)

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- {length} files added to dataset -- insert response: {response_arr}")

            return {"message": f"Success: {length} files added to dataset"}
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError(f"Failed to add file to dataset", 404)