from flask import Blueprint, current_app, g, json, request

from api.files.handler.request_upload_files import RequestUploadFiles


files_api = Blueprint('files_api', __name__)

# UPLOAD FILE
@files_api.route('/files/upload', methods=['POST'])
def upload_files():
    request_id = g.request_id
    data = request.form
    data = json.loads(data.get('data'))
    files = request.files
    api_request = RequestUploadFiles(request_id, data, files)
    response = api_request.do_process()
    return response

# GET FILE LIST
@files_api.route('/files/list', methods=['GET'])
def get_files_list():
    args = dict(request.args)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetFilesList(request_id, args)
    response = api_request.do_process()
    return response

# DOWNLOAD FILE
@files_api.route('/files/download', methods=['GET'])
def download_files():
    args = dict(request.args)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestDownloadFiles(request_id, args)
    response = api_request.do_process()
    return response

# MOVE FILE
@files_api.route('/files/move', methods=['PUT'])
def move_files():
    data = json.loads(request.data)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestMoveFiles(request_id, data)
    response = api_request.do_process()
    return response

# COPY FILE
@files_api.route('/files/copy', methods=['PUT'])
def copy_files():
    data = json.loads(request.data)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestCopyFiles(request_id, data)
    response = api_request.do_process()
    return response

# DELETE FILE
@files_api.route('/files/delete', methods=['DELETE'])
def delete_files():
    args = dict(request.args)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestDeleteFiles(request_id, args)
    response = api_request.do_process()
    return response







    
