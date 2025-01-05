import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestUpdateDatastoreUserRole(AbstractHandler):
    def __init__(self, request_id: str, user_id: str, payload: dict):
        self.request_id = request_id
        self.user_id = user_id
        self.payload = payload

    def do_process(self):
        try:
    
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} -- user_id: {self.user_id} -- PAYLOAD: {self.payload}")

            # Update user role
            dao_request = Request()
            update_user_role_response = dao_request.update(self.request_id, Constant.table["DATASTORE_ROLES"], "user_id", self.user_id, self.payload)

            if not update_user_role_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: UPDATE_DATASTORE_USER_ROLE --- ERROR: Failed to update datastore user role")
                raise ThrowError("Failed to update datastore user role", 500)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: UPDATE_DATASTORE_USER_ROLE --- RESPONSE: {update_user_role_response['response']}")

            return update_user_role_response['response']
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to update datastore user role", 500)