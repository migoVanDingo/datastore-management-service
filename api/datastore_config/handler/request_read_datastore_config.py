import traceback
from flask import current_app
from interface.abstract_handler import AbstractHandler
from utility.constant import Constant
from utility.error import ThrowError
from utility.request import Request


class RequestReadDatastoreConfig(AbstractHandler):
    def __init__(self, request_id: str, args: dict):
        super().__init__()
        self.request_id = request_id
        self.args = args

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {__name__} --- Read Datastore Config -- args: {self.args}")
            dao_request = Request()
            config_response = dao_request.read_list(self.request_id, Constant.table["DATASTORE_CONFIG"], self.args)

            if "response" not in config_response:
                current_app.logger.error(f"{self.request_id} --- {__name__} --- Read Datastore Config -- ERROR: Datastore Config not found")
                raise Exception("Datastore Config not found", 404)
            
            for config in config_response["response"]:
                field_name = config["field_name"]
                query = f"SELECT DISTINCT {field_name} FROM aolme_videos ORDER BY {field_name}"
                options_response = dao_request.query(self.request_id, query)
                result = []
                for option in options_response["response"]:
                    result.append(option[field_name])
                config["field_options"] = result

            current_app.logger.info(f"{self.request_id} --- {__name__} --- Read Datastore Config -- RESPONSE: {config_response}")

            return config_response["response"]

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {__name__} --- {traceback.format_exc()} --- {e}")
            raise ThrowError(f"Internal Server Error -- {e}", 500)