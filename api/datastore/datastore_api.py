from flask import Blueprint, current_app, g, json, request

from api.datastore.handler.request_create_datastore import RequestCreateDatastore


datastore_api = Blueprint('datastore_api', __name__)

# Create datastore
@datastore_api.route('/datastore', methods=['POST'])
def create_datastore():
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")

    data = json.loads(request.data)
    api_request = RequestCreateDatastore(data)
    response = api_request.do_process()
    
    return "NOT_IMPLEMENTED"


# Get datastore
## -> by id
@datastore_api.route('/datastore', methods=['GET'])
def get_datastore_by_id(id):
    args = request.args
    return "NOT_IMPLEMENTED"

# Update datastore
@datastore_api.route('/datastore/<string:id>', methods=['PUT'])
def update_datastore(id):
    data = json.loads(request.data)

    return "NOT_IMPLEMENTED"

# Delete datastore
@datastore_api.route('/datastore/<string:id>', methods=['DELETE'])
def delete_datastore(id):
    return "NOT_IMPLEMENTED"

# Get all datastores
## -> by user
@datastore_api.route('/datastore/list', methods=['GET'])
def get_datastores_by_user(id):
    args = request.args
    return "NOT_IMPLEMENTED"
