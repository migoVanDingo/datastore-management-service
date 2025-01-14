from flask import Blueprint, current_app, g, json, request

from api.datastore_config.handler.request_create_dateastore_config import RequestCreateDatastoreConfig
from api.datastore_config.handler.request_delete_datastore_config import RequestDeleteDatastoreConfig
from api.datastore_config.handler.request_read_datastore_config import RequestReadDatastoreConfig
from api.datastore_config.handler.request_read_list_datastore_config import RequestReadListDatastoreConfig
from api.datastore_config.handler.request_update_datastore_config import RequestUpdateDatastoreConfig


datastore_config_api = Blueprint('datastore_config_api', __name__)

@datastore_config_api.route('/datastore-config/create', methods=['POST'])
def create_datastore_config():
    data = json.loads(request.data)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestCreateDatastoreConfig(request_id, data)
    return api_request.do_process()

@datastore_config_api.route('/datastore-config/read', methods=['GET'])
def read_datastore_config():
    args = request.args.to_dict()
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestReadDatastoreConfig(request_id, args)
    return api_request.do_process()

@datastore_config_api.route('/datastore-config/list', methods=['GET'])
def read_list_datastore_config():
    args = request.args.to_dict()
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestReadListDatastoreConfig(request_id, args)
    return api_request.do_process()

@datastore_config_api.route('/datastore-config/update', methods=['PUT'])
def update_datastore_config():
    data = json.loads(request.data)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestUpdateDatastoreConfig(request_id, data)
    return api_request.do_process()

@datastore_config_api.route('/datastore-config/delete', methods=['DELETE'])
def delete_datastore_config():
    args = request.args.to_dict()
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestDeleteDatastoreConfig(request_id, args)
    return api_request.do_process()
