import os
import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError
from utility.request import Request


class RequestCopyFiles(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- RequestCopyFiles Payload: {self.payload}")

            # Check for required fields
            if "temp_output_path" not in self.payload or self.payload["temp_output_path"] == "":
                return {"status": "ERROR", "message": "Missing temp_output_path in payload"}
            if "json_file_name" not in self.payload or self.payload["json_file_name"] == "":
                return {"status": "ERROR", "message": "Missing json_file_name in payload"}
            
            # Check if destination exists
            if "label_output_directory" not in self.payload or self.payload["label_output_directory"] == "":
                return {"status": "ERROR", "message": "Missing label_output_directory in payload"}
            
            # Check if files exists
            file_path = os.path.join(self.payload["temp_output_path"], self.payload["json_file_name"])
            if not os.path.exists(file_path):
                return {"status": "ERROR", "message": "File does not exist"}
            
            # Copy file from temp_output_path to label_output_directory
            annotation_destination_path = os.path.join(self.payload["label_output_directory"], self.payload["json_file_name"])
            os.system(f"cp {file_path} {annotation_destination_path}")

            dao_request = Request()
            # Insert file into files table
            file_insert_response = dao_request.insert(self.request_id, "files", {"datastore_id": self.payload["datastore_id"], "dataset_id": self.payload["dataset_id"], "file_path": annotation_destination_path, "file_type": "annotation", "file_name": self.payload["json_file_name"], "create_method": "LABELER", "created_by": self.payload["user_id"]})  

            # Link file to dataset_files table
            dataset_file_insert_response = dao_request.insert(self.request_id, "dataset_files", {"dataset_id": self.payload["dataset_id"], "file_id": file_insert_response["response"]["file_id"], "set_id": self.payload["set_id"], "file_type": "annotation", "created_by": self.payload["user_id"]})

            if "response" not in dataset_file_insert_response or not dataset_file_insert_response["response"]:
                raise Exception(f"Failed to link file to dataset_files table")

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- Files copied successfully")
            
            return {"status": "SUCCESS", "data": {"annotation_destination_path": annotation_destination_path, "file_id": file_insert_response["response"]["file_id"]}}
            

            
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            return {"status": "FAILED", "message": f"{e}"}