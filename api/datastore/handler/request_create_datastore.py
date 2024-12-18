import os
import traceback
from flask import current_app
from typing import Optional
from pydantic import BaseModel, ValidationError
from interface.abstract_handler import AbstractHandler
from dotenv import load_dotenv

from utility.error import ThrowError
load_dotenv()

class PayloadCreateDatastore(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: str
    is_active: bool = True
    tags: Optional[list[str]] = None


class RequestCreateDatastore(AbstractHandler):
    def __init__(self, request_id: str, payload):
        self.request_id = request_id
        self.payload = payload

    def do_process(self):
        try:
            current_app.logger.info(f"{self.request_id} --- {self.__class__.__name__} --- PAYLOAD: {self.payload}")

            # Insert datastore into DB and generate ID

            # Create Directory structure

            # Create metadata file




            return None
        except Exception as e:
            current_app.logger.error(f"{self.request_id} --- {self.__class__.__name__} --- {traceback.format_exc()} --- {e}")
            if os.environ["DEBUG"] == "True":
                print(f"{traceback.format_exc()} --- Error: {e}")
                
            raise ThrowError("Failed to create datastore", 500)
            
            
   