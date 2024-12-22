from pathlib import Path
from typing import IO, Optional
from flask import current_app
from utility.constant import Constant
from utility.payload.file_payload import FilePayload
from utility.payload.request_payload import RequestPayload
from utility.request import Request


class FileHandler:
    def __init__(self):
        pass

    
    def save_file_dir(self, request_id: str, path: str, file: IO):
        try:
            # Ensure the directory exists
            directory = Path(path)
            directory.mkdir(parents=True, exist_ok=True)

            # Construct full file path
            file_path = directory / file.filename

            # Save the file to the filesystem
            with open(file_path, "wb") as f:
                for chunk in file:
                    f.write(chunk)

            # Log successful file save
            current_app.logger.info(f"{request_id} --- {__name__} --- File saved: {file_path}")
            return str(file_path)  # Return the saved file path for reference

        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__name__} --- Error: File NOT saved -- {e}")
            raise Exception(f"Error saving file: {e}")
        

    def save_file_db(self, request_id: str, payload: dict):
        try:
            # Form payload for saving file record
            file_payload = FilePayload.form_save_file_payload(payload)


            # Form request payload
            request_payload = RequestPayload.form_insert_payload(request_id, Constant.table["FILES"], Constant.service, file_payload)


            # Save record in database
            dao_request = Request()
            response = dao_request.insert(request_id, Constant.table["FILES"], request_payload)

            current_app.logger.info(f"{request_id} --- {__name__} --- File record saved: {response['response']}")

            return response['response']
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__name__} --- File record NOT saved: {e}")
            raise Exception(f"Error saving file: {e}")
        
    def get_destination_dir(self, request_id: str, file_type: str, datastore_id: str, dataset_id: Optional[str] = None):
        try:
            # Get datastore record
            dao_request = Request()
            dao_response = dao_request.read(request_id, Constant.table["DATASTORE"], {"datastore_id": datastore_id})

            # Get dataset record
            if dataset_id:
                dao_response = dao_request.read(request_id, Constant.table["DATASET"], {"dataset_id": dataset_id})

            # Get destination directory
            destination_dir = dao_response["response"]["path"] + Constant.delimeter["DATASTORE"] + file_type

            return destination_dir
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__name__} --- Error: {e}")
            raise Exception(f"Error getting destination directory: {e}")

    
