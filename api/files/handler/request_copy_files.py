import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError


class RequestCopyFiles(AbstractHandler):
    def __init__(self, request_id: str, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:
            raise NotImplementedError
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError("Failed to copy files", 500)