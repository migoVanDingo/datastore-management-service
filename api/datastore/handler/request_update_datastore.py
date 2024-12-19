import traceback
from flask import current_app
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