import os
import traceback
from flask import current_app
import requests


class Download:
    @staticmethod
    def download_file(self, file_link, directory, file):
        try:
            
            current_app.logger.debug(f"{self.__class__.__name__} - Downloading... {file_link} to {os.path.join(directory, file)}")

            r = requests.get(file_link, stream=True)

            with open(os.path.join(directory, file), 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)


            #self.add_to_subset_items(self.ds_subset_id, file["file_id"], file["file_name"], self.owner, os.path.join(directory, file["file_name"]), "file")

            current_app.logger.debug(f"{self.__class__.__name__} - Download Complete!! {file_link} to {os.path.join(directory, file)}")

            return True
        except Exception as e:
            current_app.logger.error(f"{self.__class__.__name__} :::: {traceback.format_exc()} -- {e}")
            return False