import traceback
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
    
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- datastore_id: {self.args}")

            dao_request = Request()
            datastore_users_response = dao_request.read_list(self.request_id, Constant.table["DATASTORE_ROLES"], self.args)

            if not datastore_users_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASTORE_USERS --- ERROR: Failed to get datastore users")
                raise ThrowError("Failed to get datastore users", 500)
            
            

            for item in datastore_users_response['response']:
                # Get Datastore details
                datastore_details_response = dao_request.read(self.request_id, Constant.table["DATASTORE"], {"datastore_id": item["datastore_id"]})
                item["name"] = datastore_details_response["response"]["name"]
                item["description"] = datastore_details_response["response"]["description"]
                item["updated_at"] = datastore_details_response["response"]["updated_at"]
                item["created_at"] = datastore_details_response["response"]["created_at"]

            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GetDatastoreList --- RESPONSE: {datastore_users_response['response']}")

            return datastore_users_response['response']

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to get datastore users", 500)