import os
import traceback

from flask import current_app
from api.dataset.handler.request_get_dataset import RequestGetDataset
from api.dataset.payload.payload_get_dataset_path import PayloadGetDatasetPath
from api.datastore.handler.request_get_datastore import RequestGetDatastore
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError


class RequestGetDatasetPath(AbstractHandler):
    def __init__(self, request_id: str, payload: PayloadGetDatasetPath):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- GET_DATASET_PATH: {self.payload}")

    
            # Get dataset
            dataset_id = self.payload['dataset_id']
            datastore_id = self.payload['datastore_id']
            directory = self.payload['directory']
            
            # Use get dataset class
            dao_request = RequestGetDataset(self.request_id, {"dataset_id": dataset_id})
            dataset = dao_request.do_process()

            if "path" not in dataset:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- Dataset path not found")
                raise Exception(f"{self.request_id} --- Dataset path not found")
            
            # Get Datastore
            dao_request = RequestGetDatastore(self.request_id, {"datastore_id": datastore_id})
            datastore = dao_request.do_process()
            
            if "path" not in datastore:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- Datastore path not found")
                raise Exception(f"{self.request_id} --- Datastore path not found")

            # Form directory path
            directory_path = os.path.join(Constant.datastore_root_dir, datastore["path"], dataset["path"], directory)

            current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- Dataset Directory Path: {directory_path}")

            return { "status": "SUCCESS", "data": {"dataset_directory_path": directory_path}}



        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return { "status": "FAILED", "error": str(e) }