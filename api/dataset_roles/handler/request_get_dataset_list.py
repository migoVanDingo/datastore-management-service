import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestGetDatasetList(AbstractHandler):
    def __init__(self, request_id: str, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:
    
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- dataset_id: {self.args}")

            dao_request = Request()
            dataset_users_response = dao_request.read_list(self.request_id, Constant.table["DATASET_ROLES"], self.args)

            if not dataset_users_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASET_USERS --- ERROR: Failed to get dataset users")
                raise ThrowError("Failed to get dataset users", 500)
            
            

            for item in dataset_users_response['response']:
                # Get Dataset details
                dataset_details_response = dao_request.read(self.request_id, Constant.table["DATASET"], {"dataset_id": item["dataset_id"]})
                item["name"] = dataset_details_response["response"]["name"]
                item["description"] = dataset_details_response["response"]["description"]
                item["updated_at"] = dataset_details_response["response"]["updated_at"]
                item["created_at"] = dataset_details_response["response"]["created_at"]

            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GetDatasetList --- RESPONSE: {dataset_users_response['response']}")

            return dataset_users_response['response']

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to get dataset users", 500)