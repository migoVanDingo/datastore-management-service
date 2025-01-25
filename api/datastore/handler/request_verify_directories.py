import os
import traceback

from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant


class RequestVerifyDirectories(AbstractHandler):
    def __init__(self, request_id: str, payload: dict):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:

            current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- VERIFY_DIRECTORIES_PAYLOAD: {self.payload}")

            # Get dataset_directory_path
            dataset_directory_path = self.payload['dataset_directory_path']

            #Verify if the directory exists
            if not os.path.exists(dataset_directory_path):
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- Dataset directory not found")
                raise Exception(f"{self.request_id} --- Dataset directory not found")

            # Output Directory 
            output_parent_directory = self.payload["set_name"] + "__" + self.payload["project_name"]
            for dir in Constant.dataset["ANNOTATION"]["DIRECTORY"].values():
                output_directory = os.path.join(dataset_directory_path, output_parent_directory, dir)
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory, exist_ok=True)
                    current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- Output Directory created: {output_directory}")

                else:
                    current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- Output Directory exists: {output_directory}")

            label_output_directory = os.path.join(dataset_directory_path, output_parent_directory, Constant.dataset["ANNOTATION"]["DIRECTORY"]["LABELER_OUTPUT"])
            processed_directory =  os.path.join(dataset_directory_path, output_parent_directory, Constant.dataset["ANNOTATION"]["DIRECTORY"]["PROCESSED"])

            current_app.logger.debug(f"{self.request_id} --- {self.__class__.__name__} --- VERIFY_DIRECTORIES_RESPONSE --- label_output_directory: {label_output_directory} --- processed_directory: {processed_directory}")

            return {"status": "SUCCESS", "data": {"label_output_directory": label_output_directory, "processed_directory": processed_directory}}

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {str(e)}")
            return {"status": "FAILED", "error": str(e)}