import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError


class RequestUpdateDatastoreConfig(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        super().__init__()
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {__name__} --- Update Datastore Config -- PAYLOAD: {self.payload}")
            raise ThrowError("NOT_IMPLEMENTED", 501)
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {__name__} --- {traceback.format_exc()} --- {e}")
            return "NOT_IMPLEMENTED"