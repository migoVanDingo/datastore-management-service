import traceback

from flask import current_app
from interface.abstract_handler import AbstractHandler


class RequestAddAnnotationToDataset(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- ADD_ANNOTATION_TO_DATASET_PAYLOAD: {self.payload}")

            return 'NOT_IMPLEMENTED'

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}