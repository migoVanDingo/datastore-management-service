from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError
from utility.request import Request


class RequestDeleteDatastore(AbstractHandler):
    def __init__(self, request_id: str, datastore_id: str):
        self.request_id = request_id
        self.datastore_id = datastore_id

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- ARGS: {self.datastore_id}")

            dao_request = Request()
            dao_response = dao_request.delete(self.request_id, "datastore", self.datastore_id)

            if not dao_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DELETE_DATASTORE --- ERROR: Failed to delete datastore")
                raise ThrowError("Failed to delete datastore", 500)
            
            

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DELETE_DATASTORE --- RESPONSE: {dao_response['response']}")
            if type(dao_response['response']):
                return dao_response

            return dao_response['response']
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {e}")
            raise ThrowError("Failed to delete datastore", 500)