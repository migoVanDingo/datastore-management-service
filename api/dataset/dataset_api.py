from flask import Blueprint, current_app, g, json, request

from api.dataset.handler.request_create_dataset import RequestCreateDataset
from api.dataset.handler.request_delete_dataset import RequestDeleteDataset
from api.dataset.handler.request_get_dataset import RequestGetDataset
from api.dataset.handler.request_get_dataset_list import RequestGetDatasetList
from api.dataset.handler.request_update_dataset import RequestUpdateDataset
from api.datastore.handler.request_get_datastore import RequestGetDatastore


dataset_api = Blueprint('dataset_api', __name__)

# Create dataset
@dataset_api.route('/dataset', methods=['POST'])
def create_dataset():
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")

    data = json.loads(request.data)
    api_request = RequestCreateDataset(request_id, data)
    response = api_request.do_process()
    
    return response


# Get dataset
## -> By id
@dataset_api.route('/dataset', methods=['GET'])
def get_dataset_by_id():
    args = dict(request.args)
    
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDataset(g.request_id, args)
    response = api_request.do_process()

    return response


# Get all datasets
## -> by datastore
@dataset_api.route('/dataset/list', methods=['GET'])
def get_datasets_by_datastore(id):
    args = dict(request.args)
    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestGetDatasetList(request_id, args)
    response = api_request.do_process()
    return response



# Update dataset
@dataset_api.route('/dataset/<string:id>', methods=['PUT'])
def update_dataset(id):
    data = json.loads(request.data)

    request_id = g.request_id
    current_app.logger.info(f"{request_id} --- ENDPOINT: {__name__}")
    api_request = RequestUpdateDataset(request_id, id, data)
    response = api_request.do_process()


    return response

# Delete dataset
@dataset_api.route('/dataset/<string:id>', methods=['DELETE'])
def delete_dataset(id):
    current_app.logger.info(f"{g.request_id} --- ENDPOINT: {__name__}")
    api_request = RequestDeleteDataset(g.request_id, id)
    response = api_request.do_process()
    return response






