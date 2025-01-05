import os
import traceback
from flask import current_app
from typing import Optional
from pydantic import BaseModel, ValidationError
from api.datastore_roles.handler.request_create_datastore_role import RequestCreateDatastoreRole
from classes.directory import Directory
from interface.abstract_handler import AbstractHandler
from dotenv import load_dotenv

from utility.constant import Constant
from utility.error import ThrowError
from utility.payload.datastore_payload import DatastorePayload, IInsertDatastore
from utility.request import Request
load_dotenv()

class IInsertDatastore(BaseModel):
    name: str
    description: Optional[str]
    user_id: str


class RequestCreateDatastore(AbstractHandler):
    def __init__(self, request_id: str, payload: IInsertDatastore):
        self.request_id = request_id
        self.payload = payload
        self.payload['path'] = "/tmp"

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- PAYLOAD: {self.payload}")

            # INSERT DATASTORE RECORD
            dao_request = Request()
            dao_insert_response = dao_request.insert(self.request_id, Constant.table['DATASTORE'], DatastorePayload.form_insert_payload(self.payload))

            
            #LOGGING
            if not dao_insert_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DB_INSERT --- ERROR: Failed to create datastore ref")
                raise ThrowError("Failed to create datastore ref", 500)
            if os.environ["DEBUG"] == "True":
                current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DATASTORE_CREATED --- RESPONSE: {dao_insert_response}")


            # CREATE DATASTORE DIRECTORY STRUCTURE
            datastore_path = Directory.datastore_directory_structure(self.request_id,  self.payload['name'], dao_insert_response['response']['datastore_id'], Constant.datastore['directories'])


            #LOGGING
            if not datastore_path:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_DIRECTORY --- ERROR: Failed to create directory")
                raise ThrowError("Failed to create directory", 500)
            

            # UPDATE DATASTORE PATH
            dao_request.update(self.request_id, Constant.table['DATASTORE'], "datastore_id", dao_insert_response['response']['datastore_id'], {"path": datastore_path}) 

            # REMOVE PATH FROM RESPONSE
            del dao_insert_response['response']['path']

            # CREATE DATASTORE ROLE FOR OWNER
            api_request = RequestCreateDatastoreRole(self.request_id, {"datastore_id": dao_insert_response['response']['datastore_id'], "user_id": self.payload['user_id'], "role": "OWNER", "level": 100})
            create_role_response = api_request.do_process()

            if not create_role_response:
                current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: CREATE_DATASTORE_ROLE --- ERROR: Failed to create datastore role")
                raise ThrowError(f"Failed to create datastore role for user", 500)

            # On second thought this might better to keep on backend
            # # Add role and level to response
            # dao_insert_response['response']['role'] = create_role_response['role']
            # dao_insert_response['response']['level'] = create_role_response['level']


            #LOGGING
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- ACTION: DATASTORE_CREATED --- RESPONSE: {dao_insert_response['response']}")
            

            return dao_insert_response['response']

        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            if os.environ["DEBUG"] == "True":
                print(f"{traceback.format_exc()} --- Error: {e}")
                
            raise ThrowError("Failed to create datastore", 500)
        


            
            
   