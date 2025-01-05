import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestGetDatastoreUsers(AbstractHandler):
    def __init__(self, request_id: str, datastore_id: str):
        self.request_id = request_id
        self.datastore_id = datastore_id

    def do_process(self):
        try:
    
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- datastore_id: {self.datastore_id}")

            dao_request = Request()
            datastore_users_response = dao_request.read_list(self.request_id, Constant.table["DATASTORE_ROLES"], {"datastore_id": self.datastore_id})

            if not datastore_users_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASTORE_USERS --- ERROR: Failed to get datastore users")
                raise ThrowError("Failed to get datastore users", 500)
            
            # For each user in response get user details
            for user in datastore_users_response['response']:
                user_details_response = dao_request.read(self.request_id, Constant.table["USERS"], {"user_id": user["user_id"]})
                user["user_details"] = user_details_response["response"]
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASTORE_USERS --- RESPONSE: {datastore_users_response['response']}")

            return datastore_users_response['response']


        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to get datastore users", 500)