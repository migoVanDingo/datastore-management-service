import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestGetFilesList(AbstractHandler):
    def __init__(self, request_id: str, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- {self.args}")
            # Get the list of files from the database
            dao_request = Request()
            get_list_response = dao_request.read_list(self.request_id, Constant.table["FILES"], self.args)
            
            if not get_list_response["response"]:
                raise ThrowError(f"Failed to get files list. Query Args: {self.args}", 404)
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- Files list: {get_list_response['response']}")

            return get_list_response['response']
            

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to get files list", 500)