from flask import Blueprint, current_app, g, json, request

from api.files.handler.request_add_file_to_dataset import RequestAddFileToDataset
from api.files.handler.request_copy_files import RequestCopyFiles
from api.files.handler.request_delete_files import RequestDeleteFiles
from api.files.handler.request_download_files import RequestDownloadFiles
from api.files.handler.request_get_dataset_files_list import RequestGetDatasetFilesList
from api.files.handler.request_get_files_list import RequestGetFilesList
from api.files.handler.request_move_files import RequestMoveFiles
from api.files.handler.request_search_files_metadata import RequestSearchFilesMetadata
from api.files.handler.request_upload_files import RequestUploadFiles
from utility.decorator import unavailable
from utility.migrate_files_to_datastore_files import MigrateFiles


files_api = Blueprint('files_api', __name__)


#migrate files
@files_api.route('/datastore/migrate/files', methods=['GET'])
@unavailable(message="NON-OPERATIONAL: For data migration purposes only", status_code=503)
def migrate_files():
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = MigrateFiles(request_id)
    response = api_request.do_process()
    return response

# UPLOAD FILE
@files_api.route('/datastore/file/upload', methods=['POST'])
def upload_files():
    request_id = g.request_id
    data = request.form.to_dict()
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__} -- PAYLOAD: {data}")   
    files = request.files
    api_request = RequestUploadFiles(request_id, data, files)
    response = api_request.do_process()
    return response

# GET FILE LIST
@files_api.route('/datastore/file/list', methods=['GET'])
def get_files_list():
    args = dict(request.args)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetFilesList(request_id, args)
    response = api_request.do_process()
    return response

@files_api.route('/datastore/file/search', methods=['GET'])
def search_files():
    args = dict(request.args)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestSearchFilesMetadata(request_id, args)
    response = api_request.do_process()
    return response

# DOWNLOAD FILE
@files_api.route('/datastore/file/download', methods=['GET'])
def download_files():
    args = dict(request.args)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestDownloadFiles(request_id, args)
    response = api_request.do_process()
    return response

# MOVE FILE
@files_api.route('/datastore/file/move', methods=['PUT'])
def move_files():
    data = json.loads(request.data)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestMoveFiles(request_id, data)
    response = api_request.do_process()
    return response

# COPY FILE
@files_api.route('/datastore/file/copy', methods=['PUT'])
def copy_files():
    data = json.loads(request.data)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestCopyFiles(request_id, data)
    response = api_request.do_process()
    return response

# DELETE FILE
@files_api.route('/datastore/file/delete', methods=['DELETE'])
def delete_files():
    args = dict(request.args)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestDeleteFiles(request_id, args)
    response = api_request.do_process()
    return response


#ADD FILED TO DATASET FROM DATASTORE    
@files_api.route('/datastore/file/dataset/add', methods=['POST'])
def add_file_to_dataset():
    data = json.loads(request.data)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestAddFileToDataset(request_id, data)
    response = api_request.do_process()
    return response


#GET DATASET FILES LIST
@files_api.route('/datastore/dataset/files/list', methods=['GET'])
def get_dataset_files_list():
    args = dict(request.args)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDatasetFilesList(request_id, args)
    response = api_request.do_process()
    return response








    
