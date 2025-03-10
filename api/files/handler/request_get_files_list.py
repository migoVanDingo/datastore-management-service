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

            # Get the list of refs from the dataset_files table
            ds_files_response = dao_request.read_list(self.request_id, Constant.table["DATASET_FILES"], self.args)
            
            if not ds_files_response["response"]:
                return []

            files = []    
            # For each ref use the file_id to get the file from the files table
            for ds_file in ds_files_response["response"]:
                file_response = dao_request.read(self.request_id, Constant.table["FILES"], {"file_id": ds_file["file_id"]})
                files.append(file_response["response"])

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- Files list: {files}")

            return files
            

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError(f"Failed to get files list. Query Args: {self.args}", 404)