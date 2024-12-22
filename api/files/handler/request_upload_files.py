from typing import IO, Optional
from flask import current_app
from pydantic import BaseModel
from classes.file_handler import FileHandler
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError

class IUploadFile(BaseModel):
    datastore_id: str
    dataset_id: Optional[str] = None
    file_name: str
    file_type: str
    metadata: Optional[str] = None

class RequestUploadFiles(AbstractHandler):
    def __init__(self, request_id: str, payload: IUploadFile, files: list[IO]):
        super().__init__()
        self.payload = payload
        self.request_id = request_id
        self.files = files

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {__name__} --- Uploading files -- PAYLOAD: {self.payload}")

            if 'file' not in self.files:
                raise ThrowError("No file part", 400)
            
            file_handler = FileHandler()
            
            # For each file, save it to filesystem and save record in database
            for file in self.files:
                file_handler.save_file_dir(self.request_id, self.payload['file_path'], file)
                file_handler.save_file_db(self.request_id, self.payload)    

            response = {"message": "Files uploaded successfully", "status": 200}
            return response
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {__name__} --- {e}")
            raise ThrowError(f"There was an error uploading files. {e}", 500)
        