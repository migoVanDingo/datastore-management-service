import os
import traceback
from flask import current_app
from classes.directory import Directory
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.payload.request_payload import RequestPayload
from utility.request import Request


class RequestUpdateDatastore(AbstractHandler):
    def __init__(self, request_id: str, datastore_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload
        self.datastore_id = datastore_id

    def do_process(self):
        
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- PAYLOAD: {self.payload}")

            if "name" in self.payload: 
                # Get datastore
                dao_request = Request()
                dao_response = dao_request.read(self.request_id, Constant.table['DATASTORE'], {"datastore_id": self.datastore_id})
                old_path = dao_response['response']['path']
                new_path = self.payload['name'] + Constant.delimeter['DATASTORE'] + self.datastore_id
                Directory.update_directory(self.request_id, old_path, new_path)
                self.payload['path'] = new_path

                # GET DATASETS OF DATASTORE
                dao_request = Request()
                dao_response = dao_request.read_list(self.request_id, Constant.table['DATASET'], {"datastore_id": self.datastore_id})
                if dao_response['response']:
                    for dataset in dao_response['response']:
  
                        old_path_dataset = dataset['path']
                        splits = old_path_dataset.split("/")
                        
                        # shift split
                        old_path_component = "/".join(splits[1:])
                        new_path_dataset = os.path.join(new_path, old_path_component)
                    
                        dao_request.update(self.request_id, Constant.table['DATASET'], "dataset_id", dataset['dataset_id'], {"path": new_path_dataset})
            
            # Update datastore into DB
            dao_request = Request()
            dao_update_response = dao_request.update(self.request_id, Constant.table['DATASTORE'], "datastore_id", self.datastore_id , self.payload)

            if not dao_update_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DB_UPDATE --- ERROR: Failed to update datastore")
                raise ThrowError("Failed to update datastore", 500)
            
            

            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DATASTORE_UPDATED --- RESPONSE: {dao_update_response['response']}")

            if type(dao_update_response['response']):
                return dao_update_response

            return dao_update_response['response']
        
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to update datastore", 500)