import traceback

from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError
from utility.payload.file_payload import FilePayload
from utility.request import Request


class MigrateFiles(AbstractHandler):
    def __init__(self, request_id: str):
        self.request_id = request_id
    

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__}")
            # Get the list of files from the database

            query = "SELECT datastore_id, file_id, created_by FROM files"
            dao_request = Request()
            get_list_response = dao_request.query(self.request_id, query)

            if not get_list_response["response"]:
                return []
            
            count = 0
            for file in get_list_response['response']:
                payload = FilePayload.form_insert_datastore_file_payload(file)
                dao_request.insert(self.request_id, "datastore_files", payload)
                count += 1
                print(f"count: {count}")
                
            
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} ---  --- {count} files migrated")
            print("DONE")

            return "SUCCESS!"  
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError(f"Failed to migrate files", 404)