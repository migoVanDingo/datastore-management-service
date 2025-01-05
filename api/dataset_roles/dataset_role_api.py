from flask import Blueprint, current_app, g, json, request


from api.dataset_roles.handler.request_create_dataset_role import RequestCreateDatasetRole
from api.dataset_roles.handler.request_get_dataset_list import RequestGetDatasetList
from api.dataset_roles.handler.request_get_dataset_user_role import RequestGetDatasetUserRole
from api.dataset_roles.handler.request_get_dataset_users import RequestGetDatasetUsers
from api.dataset_roles.handler.request_update_dataset_user_role import RequestUpdateDatasetUserRole


dataset_role_api = Blueprint('dataset_role_api', __name__)

# Create dataset role
@dataset_role_api.route('/dataset/role', methods=['POST'])
def create_dataset_role():
    request_id = g.request_id
    data = json.loads(request.data)
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestCreateDatasetRole(request_id, data)
    response = api_request.do_process()
    return response


# Get dataset role
## -> by user_id
@dataset_role_api.route('/dataset/<string:dataset_id>/role/<string:user_id>', methods=['GET'])
def get_dataset_user_role(dataset_id, user_id):
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDatasetUserRole(request_id, dataset_id, user_id)
    response = api_request.do_process()
    return response

# Get dataset list for user
@dataset_role_api.route('/dataset/roles/list', methods=['GET'])
def get_dataset_list():
    args = request.args.to_dict()
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDatasetList(request_id, args)
    response = api_request.do_process()
    return response


# Get dataset user list
@dataset_role_api.route('/dataset/<string:dataset_id>/list', methods=['GET'])
def get_dataset_user_list(dataset_id):
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDatasetUsers(request_id, dataset_id)
    response = api_request.do_process()
    return response


# Update dataset role
@dataset_role_api.route('/dataset/role', methods=['PUT'])
def update_dataset_user_role():
    request_id = g.request_id
    data = json.loads(request.data)
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestUpdateDatasetUserRole(request_id, data)
    response = api_request.do_process()
    return response
