from typing import Optional
from flask import current_app
from pydantic import BaseModel
from classes.directory import Directory
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request

class IInsertDataset(BaseModel):
    name: str
    description: Optional[str]
    datastore_id: str


class RequestCreateDataset(AbstractHandler):
    def __init__(self, request_id: str, payload: IInsertDataset):
        self.request_id = request_id
        self.payload = payload
        self.payload['path'] = '/tmp'

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- PAYLOAD: {self.payload}")

            # GET DATASTORE RECORD
            dao_request = Request()
            dao_response = dao_request.read(self.request_id, Constant.table['DATASTORE'], {"datastore_id": self.payload['datastore_id']})
            datastore_path = dao_response['response']['path']

            # INSERT DATASET RECORD
            dao_request = Request()
            dao_response = dao_request.insert(self.request_id, Constant.table['DATASET'], self.payload)

            if not dao_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_DATASET --- ERROR: Failed to create dataset")
                raise ThrowError("Failed to create dataset", 500)
            
            # CREATE DATASET DIRECTORY STRUCTURE
            self.payload['path'] = datastore_path
            dataset_path = Directory.dataset_directory_structure(self.request_id, self.payload['path'], self.payload['name'], dao_response['response']['dataset_id'], Constant.dataset['directories'])

            if not dataset_path:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_DIRECTORY --- ERROR: Failed to create directory")
                raise ThrowError("Failed to create directory", 500)
            
            # UPDATE DATASET PATH
            
            dao_request.update(self.request_id, Constant.table['DATASET'], "dataset_id", dao_response['response']['dataset_id'], {"path": dataset_path})
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_DATASET --- RESPONSE: {dao_response['response']}")

            del dao_response['response']['path']
            
            return dao_response['response']
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {e}")
            raise ThrowError("Failed to create dataset", 500)