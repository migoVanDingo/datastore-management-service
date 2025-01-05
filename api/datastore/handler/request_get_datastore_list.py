from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestGetDatastoreList(AbstractHandler):
    def __init__(self, request_id: str, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- ARGS: {self.args}")

            dao_request = Request()

            
            table = Constant.table["DATASTORE"]

            dao_response = dao_request.read_list(self.request_id, table, self.args)

            if not dao_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASTORE --- ERROR: Failed to get datastore")
                raise ThrowError("Failed to get datastore", 500)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASTORE_LIST --- RESPONSE: {dao_response['response']}")

            return dao_response['response']
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {e}")
            raise ThrowError("Failed to get datastore", 500)

