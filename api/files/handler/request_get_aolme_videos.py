import traceback

from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.request import Request


class RequestGetAolmeVideos(AbstractHandler):
    def __init__(self, request_id: str):
        self.request_id = request_id

    def do_process(self):
        try:
            
            current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- GET_AOLME_VIDEOS_PAYLOAD")

            dao_request = Request()
            dao_response = dao_request.query(self.request_id, "SELECT * FROM aolme_videos")

            if "response" not in dao_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: GET_AOLME_VIDEOS --- ERROR: Failed to get aolme videos")
                raise Exception("Failed to get aolme videos")
        
            return {"status": "SUCCESS", "data": dao_response["response"]}
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}