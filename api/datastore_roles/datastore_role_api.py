from flask import Blueprint, current_app, g, json, request


from api.datastore_roles.handler.request_create_datastore_role import RequestCreateDatastoreRole
from api.datastore_roles.handler.request_get_datastore_list import RequestGetDatastoreList
from api.datastore_roles.handler.request_get_datastore_user_role import RequestGetDatastoreUserRole
from api.datastore_roles.handler.request_get_datastore_users import RequestGetDatastoreUsers
from api.datastore_roles.handler.request_update_datastore_user_role import RequestUpdateDatastoreUserRole


datastore_role_api = Blueprint('datastore_role_api', __name__)

# Create datastore role
@datastore_role_api.route('/datastore/role', methods=['POST'])
def create_datastore_role():
    request_id = g.request_id
    data = json.loads(request.data)
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestCreateDatastoreRole(request_id, data)
    response = api_request.do_process()
    return response


# Get datastore role
## -> by user_id
@datastore_role_api.route('/datastore/<string:datastore_id>/role/<string:user_id>', methods=['GET'])
def get_datastore_user_role(datastore_id, user_id):
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDatastoreUserRole(request_id, datastore_id, user_id)
    response = api_request.do_process()
    return response

# Get datastore list for user
@datastore_role_api.route('/datastore/roles/list', methods=['GET'])
def get_datastore_list():
    args = request.args.to_dict()
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDatastoreList(request_id, args)
    response = api_request.do_process()
    return response


# Get datastore user list
@datastore_role_api.route('/datastore/<string:datastore_id>/list', methods=['GET'])
def get_datastore_user_list(datastore_id):
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDatastoreUsers(request_id, datastore_id)
    response = api_request.do_process()
    return response


# Update datastore role
@datastore_role_api.route('/datastore/role', methods=['PUT'])
def update_datastore_user_role():
    request_id = g.request_id
    data = json.loads(request.data)
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestUpdateDatastoreUserRole(request_id, data)
    response = api_request.do_process()
    return response
