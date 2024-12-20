import os
import traceback

from flask import current_app

from utility.constant import Constant


class Directory:

    @staticmethod
    def create_directory(request_id, path):
        try:
            os.makedirs(os.path.join(Constant.datastore_root_dir, path), exist_ok=True)
            return True
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__class__.__name__} --- {traceback.format_exc()} --- {e}")
            return False
        
    @staticmethod
    def update_directory(request_id, path, new_path):
        try:
            os.rename(os.path.join(Constant.datastore_root_dir, path), os.path.join(Constant.datastore_root_dir, new_path))
            return True
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__class__.__name__} --- {traceback.format_exc()} --- {e}")
            return False
        
    @staticmethod
    def datastore_directory_structure(request_id, name, id, directories):
        """
        Creates a directory structure and its child directories.
        
        Parameters:
            request_id (str): Request ID
            name (str): The name of the entity.
            id (str): The ID of the entity.
            directories (list): A list of directories to be created.
            metadata_file (str): The name of the metadata file.
        
        Returns:
            str: The path to the created entity directory.
        """
        try:
            # Define the entity directory structure
            datastore_path = name + Constant.delimeter['DATASTORE'] + id
            
            # Create the directories
            for directory in directories:
                path = os.path.join(datastore_path, directory)
                Directory.create_directory(request_id, path)
            
            Directory.create_metadata_file(request_id, datastore_path, datastore_path)
            return datastore_path
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__class__.__name__} --- {traceback.format_exc()} --- {e}")
            return False
        
    @staticmethod
    def dataset_directory_structure(request_id, datastore_path, name, id, directories):
        """
        Creates a directory structure and its child directories.
        
        Parameters:
            request_id (str): Request ID
            name (str): The name of the entity.
            id (str): The ID of the entity.
            directories (list): A list of directories to be created.
            metadata_file (str): The name of the metadata file.
        
        Returns:
            str: The path to the created entity directory.
        """
        try:
            # Define the entity directory structure
            name =  name + Constant.delimeter['DATASET'] + id
            dataset_path = os.path.join(datastore_path, "datasets", name)
            
            # Create the directories
            for directory in directories:
                path = os.path.join(dataset_path, directory)
                Directory.create_directory(request_id, path)
            
            Directory.create_metadata_file(request_id, dataset_path, name)
            return dataset_path
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__class__.__name__} --- {traceback.format_exc()} --- {e}")
            return False  

      
        
    @staticmethod
    def create_metadata_file(request_id, path, name):
        try:
            # Create the metadata file
            metadata_file = os.path.join(os.environ['DATASTORE_ROOT'], path, name + Constant.files['metadata'])
            current_app.logger.info(f"{request_id} --- {__class__.__name__} --- METADATA FILE: {metadata_file}")
            with open(metadata_file, "w") as f:
                f.write("{}")  # Placeholder for metadata content
            return True
        except Exception as e:
            current_app.logger.error(f"{request_id} --- {__class__.__name__} --- {traceback.format_exc()} --- {e}")
            return False