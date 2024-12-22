from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError
from utility.request import Request


class RequestGetDatasetList(AbstractHandler):
    def __init__(self, request_id: str, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- ARGS: {self.args}")

            dao_request = Request()
            dao_response = dao_request.read_list(self.request_id, "dataset", self.args)

            if not dao_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASET_LIST --- ERROR: Failed to get dataset list")
                raise ThrowError("Failed to get dataset list", 500)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASET_LIST --- RESPONSE: {dao_response['response']}")

            return dao_response['response']
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {e}")
            raise ThrowError("Failed to get dataset list", 500)