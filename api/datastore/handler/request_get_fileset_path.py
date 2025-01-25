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

"""
Class RequestVerifyFileset:
    - This class verifies that the fileset exists in the datastore
    - That means, the proper raw datafiles are in the proper directory corresponding to its set_id
    - If the file does not exist, and if file is of type LINK it will download the file. The link to download is in the URL field of the metadata JSON field which is stored in the "files" table.
    - If the file does not exist, and if file is not of type LINK, it will throw an error.
    - So if you've added a file manually (not through the app), you'll need to:
        -> add the file to the proper set directory
        -> add  a record in the "files" table with the proper metadata.
        -> add a record to the "dataset_files" table with the proper set_id
        -> To avoid all of this, it would be best to upload the file through the app. This will automatically add the file to the proper set directory and add the proper records to the "files" and "dataset_files" tables.

    Payload Example:
    class IVerifyFileset(BaseModel):
        datastore_id: str
        set_id: str
        data_type: str

    Return Example:
    class ReturnVerifyFileset:
        set_path: str
"""




class RequestGetFilesetPath(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- GET_DATASTORE_SET_DIRECTORY: {self.payload}")

            # Use datastore_id to get the datastore directory
            datastore_id = self.payload['datastore_id']
            dao_request = Request()
            datastore_response = dao_request.read(self.request_id, 'datastore', {"datastore_id": datastore_id})

            if not datastore_response or not datastore_response["response"]:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- Datastore not found")
                raise Exception(f"{self.request_id} --- Datastore not found")
            
            # Check if the datastore directory exists
            datastore_directory = os.path.join(Constant.datastore_root_dir, datastore_response["response"]["path"])
            if not datastore_directory:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- Datastore directory not found")
                raise Exception(f"{self.request_id} --- Datastore directory not found")
            
            set_id = self.payload['set_id']
            set_type = self.payload['data_type']

            current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- Set ID: {set_id} --- Set Type: {set_type} --- Datastore Directory: {datastore_directory}")
            set_path = os.path.join(datastore_directory, "raw_data", set_type, set_id)

            # Check if directory exists
            if not os.path.exists(set_path):
                os.makedirs(set_path)
            
            return { "status": "SUCCESS", "data": {"set_path": set_path}}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return { "status": "FAILED", "error": str(e) }
