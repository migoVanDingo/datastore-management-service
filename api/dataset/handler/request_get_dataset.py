from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestGetDataset(AbstractHandler):
    def __init__(self, request_id: str, dataset_id: str):
        self.request_id = request_id
        self.dataset_id = dataset_id

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- ARGS: {self.dataset_id}")

            dao_request = Request()
            dao_response = dao_request.read(self.request_id, Constant.table["DATASET"], self.dataset_id)

            if not dao_response or "response" not in dao_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASET --- ERROR: Failed to get dataset")
                raise ThrowError("Failed to get Dataset", 500)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASET --- RESPONSE: {dao_response['response']}")

            return dao_response['response']
        
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {e}")
            raise ThrowError("Failed to get Dataset", 500)