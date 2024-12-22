import os
from pathlib import Path
import traceback
from typing import IO, Optional
from flask import current_app
from utility.constant import Constant
from utility.error import ThrowError
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
            file_path = os.path.join(Constant.datastore_root_dir, str(file_path))

            current_app.logger.info(f"{request_id} --- {__name__} --- Saving file: {file_path}")

            # Save the file to the filesystem
            with open(file_path, "wb") as f:
                for chunk in file:
                    f.write(chunk)

            # Log successful file save
            current_app.logger.info(f"{request_id} --- {__name__} --- File saved: {file_path}")
            return str(file_path)  # Return the saved file path for reference

        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__name__} --- {traceback.format_exc()} --- Error: File NOT saved -- {e}")
            raise Exception(f"Error saving file: {e}")
        

    def save_file_db(self, request_id: str, payload: dict):
        try:
            # Form payload for saving file record
            file_payload = FilePayload.form_save_file_payload(payload)

            # Save record in database
            dao_request = Request()
            response = dao_request.insert(request_id, Constant.table["FILES"], file_payload)

            current_app.logger.info(f"{request_id} --- {__name__} --- File record saved: {response['response']}")

            return response['response']
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__name__}  --- {traceback.format_exc()} ---  File record NOT saved: {e}")
            raise Exception(f"Error saving file: {e}")
        

    def get_destination_dir(self, request_id: str, file_type: str, datastore_id: str, dataset_id: Optional[str] = None):
        try:
            # Get datastore record
            dao_request = Request()

            # Get datastore record
            dao_response = dao_request.read(request_id, Constant.table["DATASTORE"], {"datastore_id": datastore_id})
            datastore = dao_response["response"]
            datastore_path = datastore["path"]
            current_app.logger.info(f"{request_id} --- {__name__} --- Datastore path: {datastore_path}")   

            if file_type in Constant.file_dir["datastore"]:
                destination_path = os.path.join(datastore_path, Constant.file_dir["datastore"][file_type])
            elif file_type in Constant.file_dir["dataset"]:
                path_suffix =  Constant.file_dir["dataset"][file_type]

                if dataset_id:
                    dao_response = dao_request.read(request_id, Constant.table["DATASET"], {"dataset_id": dataset_id})
                    dataset = dao_response["response"]
                    dataset_path = dataset["path"]
                    current_app.logger.info(f"{request_id} --- {__name__} --- Dataset path: {dataset_path}")
                    path_suffix = os.path.join(dataset_path, path_suffix)
                    destination_path = os.path.join(datastore_path, path_suffix)
                else:
                    raise ThrowError(f"No dataset_id provided for dataset file type: {file_type}", 500)
            else:
                raise ThrowError(f"Invalid file type: {file_type}", 400)

            current_app.logger.info(f"{request_id} --- {__name__} --- Destination directory: {destination_path}")

            return destination_path
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__name__}  --- {traceback.format_exc()} ---  Error: {e}")
            raise Exception(f"Error getting destination directory: {e}")
        
