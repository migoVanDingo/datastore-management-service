import json
import os
import traceback

from flask import current_app
from api.datastore.payload.payload_verify_fileset import IVerifyFileset
from api.utility.download import Download
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestVerifyFileset(AbstractHandler):
    def __init__(self, request_id: str, payload: IVerifyFileset):
        request_id = request_id
        self.payload = payload

    def do_process(self):
        try:

            # Use datastore_id to get the datastore directory
            datastore_id = self.payload['datastore_id']
            dao_request = Request()
            datastore_response = dao_request.read(self.request_id, 'datastore', {"datastore_id": datastore_id})

            if not datastore_response or not datastore_response["response"]:
                raise Exception("Datastore not found")
            
            # Check if the datastore directory exists
            datastore_directory = os.path.join(Constant.datastore_root_dir, datastore_response["response"]["path"])
            if not datastore_directory:
                raise Exception("Datastore directory not found")
            
            set_id = self.payload['set_id']
            set_type = self.payload['data_type']
            set_path = os.path.join(datastore_directory, "raw_data", set_type, set_id)

            # Check if the file set directory exists
            if not os.path.exists(set_path):
                # Make directories
                os.makedirs(set_path)

            # Files from 
            query = f"SELECT df.dataset_id, df.file_id, df.set_id, f.* FROM dataset_files df JOIN files f ON df.file_id = f.file_id WHERE df.set_id = {set_id}"

            response_files = dao_request.query(self.request_id, query)
            if not response_files or not response_files["response"]:
                raise Exception("No files found")
            
            
            for file in response_files["response"]:
                file_path = os.path.join(set_path, file["file_name"])
                if not os.path.exists(file_path):
                    # Check if create_method is LINK
                    if file["create_method"] == "LINK":
                        metadata = json.loads(file["metadata"])

                        download_link = metadata["url"]
                        if not Download.download_file(download_link, set_path, file["file_name"]):
                            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- Failed to download file: {file['file_name']}")
                            raise Exception(f"Failed to download file: {file['file_name']}")
                            

                    else:
                        raise Exception(f"File does not exist and cannot be downloaded -- ID: {file["file_id"]} --- NAME: {file['file_name']}")
                else:
                    current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- File exists: {file_path}")
            
            return {"set_path": set_path}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            raise ThrowError(f"{self.request_id} --- {self.__class__.__name__} --- {str(e)}")
