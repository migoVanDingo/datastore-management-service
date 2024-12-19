import os
import traceback

from flask import current_app

from utility.constant import Constant


class Directory:

    @staticmethod
    def create_directory(request_id, path):
        try:
            os.makedirs(os.path.join(Constant.datastore_root_dir, path))
            return True
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__class__.__name__} --- {traceback.format_exc()} --- {e}")
            return False
            