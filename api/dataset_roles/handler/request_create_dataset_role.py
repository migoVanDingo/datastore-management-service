import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.payload.dataset_payload import DatasetPayload
from utility.payload.datastore_payload import DatastorePayload
from utility.request import Request


class RequestCreateDatasetRole(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- PAYLOAD: {self.payload}")            

            dao_request = Request()
            insert_role_response = dao_request.insert(self.request_id, Constant.table["DATASET_ROLES"], DatasetPayload.form_dataset_roles_insert_payload(self.payload))
 
            if not insert_role_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_DATASTORE_ROLE --- ERROR: Failed to create dataset role")
                raise ThrowError("Failed to create dataset role", 500)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_DATASET_ROLE --- RESPONSE: {insert_role_response['response']}")

            return insert_role_response['response']


            
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to create dataset role", 500)