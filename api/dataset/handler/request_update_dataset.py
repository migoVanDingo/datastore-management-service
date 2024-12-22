import os
import traceback
from flask import current_app
from classes.directory import Directory
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestUpdateDataset(AbstractHandler):
    def __init__(self, request_id: str, dataset_id: str, payload: dict):
        self.request_id = request_id
        self.dataset_id = dataset_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- PAYLOAD: {self.payload}")

            if "name" in self.payload:
                # Get dataset
                dao_request = Request()
                dao_response = dao_request.read(self.request_id, Constant.table['DATASET'], {"dataset_id": self.dataset_id})
                old_path = dao_response['response']['path']
                splits = old_path.split("/")

                # Get datastore from dataset_id
                datastore_id = dao_response['response']['datastore_id']
                dao_datastore = Request()
                dao_response = dao_datastore.read(self.request_id, Constant.table['DATASTORE'], {"datastore_id": datastore_id})
                datastore_path = dao_response['response']['path']
                
                # all but last split
                old_path_component = "/".join(splits[:-1])
                new_path = os.path.join(old_path_component,self.payload['name'] + Constant.delimeter['DATASET'] + self.dataset_id) 

                # Update path in payload to update in DB
                self.payload['path'] = new_path

                # The following paths update the actual file system in the Directory.update_directory()
                old_path = os.path.join(datastore_path, old_path)
                new_path = os.path.join(datastore_path, new_path)
                Directory.update_directory(self.request_id, old_path, new_path)
                

            # Update dataset into DB
            dao_request = Request()
            dao_update_response = dao_request.update(self.request_id, Constant.table['DATASET'], "dataset_id", self.dataset_id, self.payload)

            if not dao_update_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DB_UPDATE --- ERROR: Failed to update dataset")
                raise ThrowError("Failed to update dataset", 500)

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DATASET_UPDATED --- RESPONSE: {dao_update_response['response']}")

            if type(dao_update_response['response']):
                return dao_update_response

            return dao_update_response['response']
        
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} -- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to update dataset", 500)