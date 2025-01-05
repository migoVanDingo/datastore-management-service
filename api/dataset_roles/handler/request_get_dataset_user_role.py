import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestGetDatasetUserRole(AbstractHandler):
    def __init__(self, request_id: str, dataset_id: str, user_id: str):
        self.request_id = request_id
        self.dataset_id = dataset_id
        self.user_id = user_id

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- dataset_id: {self.dataset_id} -- user_id: {self.user_id}")

            dao_request = Request()
            dataset_user_role_response = dao_request.read(self.request_id, Constant.table['DATASET_ROLES'], {"dataset_id": self.dataset_id, "user_id": self.user_id})

            if not dataset_user_role_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASET_USER_ROLE --- ERROR: Failed to get dataset user role")
                raise ThrowError("Failed to get dataset user role", 500)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASET_USER_ROLE --- RESPONSE: {dataset_user_role_response['response']}")

            return dataset_user_role_response['response']
        
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to get dataset user role", 500)