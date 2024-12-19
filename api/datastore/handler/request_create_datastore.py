import os
import traceback
from flask import current_app
from typing import Optional
from pydantic import BaseModel, ValidationError
from classes.directory import Directory
from interface.abstract_handler import AbstractHandler
from dotenv import load_dotenv

from utility.constant import Constant
from utility.error import ThrowError
from utility.payload.datastore_payload import IInsertDatastore
from utility.request import Request
load_dotenv()


class RequestCreateDatastore(AbstractHandler):
    def __init__(self, request_id: str, payload):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- PAYLOAD: {self.payload}")

            self.payload['path'] = "/tmp"

            # Insert datastore into DB and generate ID
            dao_request = Request()
            dao_insert_response = dao_request.insert(self.request_id, Constant.table['DATASTORE'], self.payload)

            
            if not dao_insert_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DB_INSERT --- ERROR: Failed to create datastore ref")
                raise ThrowError("Failed to create datastore ref", 500)

        
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DATASTORE_CREATED --- RESPONSE: {dao_insert_response}")

            # Create Directory structure
            datastore_id = dao_insert_response['response']['datastore_id']
            datastore_path = self.payload['name'] + Constant.delimeter['DATASTORE'] + datastore_id

            directory_request = Directory.create_directory(self.request_id, datastore_path)

            if not directory_request:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_DIRECTORY --- ERROR: Failed to create directory")
                raise ThrowError("Failed to create directory", 500)
            
            # UPDATE DATASTORE PATH
            dao_request.update(self.request_id, Constant.table['DATASTORE'], "datastore_id", datastore_id, {"path": datastore_path}) 

            del dao_insert_response['response']['path']

            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DATASTORE_CREATED --- RESPONSE: {dao_insert_response['response']}")

            return dao_insert_response['response']

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            if os.environ["DEBUG"] == "True":
                print(f"{traceback.format_exc()} --- Error: {e}")
                
            raise ThrowError("Failed to create datastore", 500)
        


            
            
   