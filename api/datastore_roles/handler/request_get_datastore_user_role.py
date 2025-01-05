import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestGetDatastoreUserRole(AbstractHandler):
    def __init__(self, request_id: str, datastore_id: str, user_id: str):
        self.request_id = request_id
        self.datastore_id = datastore_id
        self.user_id = user_id

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- datastore_id: {self.datastore_id} -- user_id: {self.user_id}")

            dao_request = Request()
            datastore_user_role_response = dao_request.read(self.request_id, Constant.table['DATASTORE_ROLES'], {"datastore_id": self.datastore_id, "user_id": self.user_id})

            if not datastore_user_role_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASTORE_USER_ROLE --- ERROR: Failed to get datastore user role")
                raise ThrowError("Failed to get datastore user role", 500)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_DATASTORE_USER_ROLE --- RESPONSE: {datastore_user_role_response['response']}")

            return datastore_user_role_response['response']
        
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to get datastore user role", 500)