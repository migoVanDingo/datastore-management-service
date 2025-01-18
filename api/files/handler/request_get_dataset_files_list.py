import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError
from utility.request import Request


class RequestGetDatasetFilesList(AbstractHandler):
    def __init__(self, request_id: str, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- {self.args}")

            dao_request = Request()
            list_response = dao_request.read_list(self.request_id, "dataset_files", self.args)

            if not list_response["response"]:
                return []
            
            files = []
            for file in list_response["response"]:
                file_response = dao_request.read(self.request_id, "files", {"file_id": file["file_id"]})
                files.append(file_response["response"])

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- Files list: {files}")

            return files

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError(f"Failed to get files list. Query Args: {self.args}", 404)