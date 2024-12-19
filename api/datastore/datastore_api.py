from flask import Blueprint, current_app, g, json, request

from api.datastore.handler.request_create_datastore import RequestCreateDatastore
from api.datastore.handler.request_delete_datastore import RequestDeleteDatastore
from api.datastore.handler.request_get_datastore import RequestGetDatastore
from api.datastore.handler.request_get_datastore_list import RequestGetDatastoreList
from api.datastore.handler.request_update_datastore import RequestUpdateDatastore


datastore_api = Blueprint('datastore_api', __name__)

# Create datastore
@datastore_api.route('/datastore', methods=['POST'])
def create_datastore():
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")

    data = json.loads(request.data)
    api_request = RequestCreateDatastore(request_id, data)
    response = api_request.do_process()
    
    return response


# Get datastore
## -> by id
@datastore_api.route('/datastore', methods=['GET'])
def get_datastore_by_id():
    args = dict(request.args)
    
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDatastore(g.request_id, args)
    response = api_request.do_process()

    return response

# Get List of datastore
@datastore_api.route('/datastore/list', methods=['GET'])
def get_all_datastore():
    args = dict(request.args)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDatastoreList(request_id, args)
    response = api_request.do_process()
    return response

# Update datastore
@datastore_api.route('/datastore/<string:id>', methods=['PUT'])
def update_datastore(id):
    data = json.loads(request.data)

    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestUpdateDatastore(request_id, id, data)
    response = api_request.do_process()


    return response

# Delete datastore
@datastore_api.route('/datastore/<string:id>', methods=['DELETE'])
def delete_datastore(id):
    current_app.logger.info(f"{g.request_id} --- ENDPOINT: {__name__}")
    api_request = RequestDeleteDatastore(g.request_id, id)
    response = api_request.do_process()
    return response


