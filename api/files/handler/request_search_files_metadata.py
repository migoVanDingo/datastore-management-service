import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.error import ThrowError
from utility.request import Request


class RequestSearchFilesMetadata(AbstractHandler):
    def __init__(self, request_id: str, args: dict):
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:
            current_app.logger.info(
                f"{self.request_id} --- {self.__class__.__name__} --- {self.args}")
            # Get the list of files from the database

            conditions = []
            for field, value in self.args.items():
                if value != "":
                    # Add the value directly into the query string
                    if field == "date" and "%20" in value:
                        # convert date epoch to date
                        value.replace("%20", " ")    
                    conditions.append(f"JSON_EXTRACT(metadata, '$.{field}') = '{value}'")

            # Final query construction
            query = "SELECT * FROM files"
            if conditions:  # Only add WHERE if there are conditions
                query += " WHERE " + " AND ".join(conditions)


            dao_request = Request()
            get_list_response = dao_request.query(self.request_id, query)

            if not get_list_response["response"]:
                return []

            current_app.logger.info(
                f"{self.request_id} --- {self.__class__.__name__} --- Files list: {get_list_response['response']}")

            return get_list_response['response']

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError(f"Failed to get files list. Query Args: {self.args}", 404)