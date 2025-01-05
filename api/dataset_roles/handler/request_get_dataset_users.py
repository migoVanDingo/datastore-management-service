import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestGetDatasetUsers(AbstractHandler):
    def __init__(self, request_id: str, dataset_id: str):
        self.request_id = request_id
        self.dataset_id = dataset_id

    def do_process(self):
        try:
    
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- dataset_id: {self.dataset_id}")

            dao_request = Request()
            dataset_users_response = dao_request.read_list(self.request_id, Constant.table["DATASET_ROLES"], {"dataset_id": self.dataset_id})

            if not dataset_users_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASET_USERS --- ERROR: Failed to get dataset users")
                raise ThrowError("Failed to get dataset users", 500)
            
            # For each user in response get user details
            for user in dataset_users_response['response']:
                user_details_response = dao_request.read(self.request_id, Constant.table["USERS"], {"user_id": user["user_id"]})
                user["user_details"] = user_details_response["response"]
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASET_USERS --- RESPONSE: {dataset_users_response['response']}")

            return dataset_users_response['response']


        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to get dataset users", 500)