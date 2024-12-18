from flask import Blueprint, json, request


dataset_api = Blueprint('dataset_api', __name__)

# Create dataset
@dataset_api.route('/dataset', methods=['POST'])
def create_dataset():
    data = json.loads(request.data)
    return "NOT_IMPLEMENTED"

# Get dataset
## -> By id
@dataset_api.route('/dataset', methods=['GET'])
def get_dataset_by_id(id):
    args = request.args
    return "NOT_IMPLEMENTED"



# Update dataset
@dataset_api.route('/dataset/<string:id>', methods=['PUT'])
def update_dataset(id):
    data = json.loads(request.data)
    return "NOT_IMPLEMENTED"

# Delete dataset
@dataset_api.route('/dataset/<string:id>', methods=['DELETE'])
def delete_dataset(id):
    return "NOT_IMPLEMENTED"



# Get all datasets
## -> by datastore
@dataset_api.route('/dataset/list', methods=['GET'])
def get_datasets_by_datastore(id):
    args = request.args
    return "NOT_IMPLEMENTED"


