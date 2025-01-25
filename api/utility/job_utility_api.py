from flask import Blueprint, g, request
import json

from api.dataset.handler.request_get_dataset_path import RequestGetDatasetPath
from api.dataset.payload.payload_get_dataset_path import PayloadGetDatasetPath
from api.datastore.handler.request_verify_directories import RequestVerifyDirectories
from api.datastore.handler.request_verify_fileset import RequestVerifyFileset
from api.datastore.payload.payload_get_fileset_path import PayloadGetFilesetPath
from api.datastore.payload.payload_verify_directories import PayloadVerifyDirectories
from api.datastore.payload.payload_verify_fileset import PayloadVerifyFileset
from api.datastore.handler.request_get_fileset_path import RequestGetFilesetPath


job_utility_api = Blueprint('job_utility_api', __name__)

# Get fileset path
@job_utility_api.route('/datastore/job/fileset/path', methods=['POST'])
def get_fileset_path():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id

    api_request = RequestGetFilesetPath(request_id, PayloadGetFilesetPath.form_payload(data))
    response = api_request.do_process()
    
    if "data" in response and response["status"] == "SUCCESS":
        res_data = response["data"]
        # merge response with data
        res_data.update(data)
        return {"status": "SUCCESS", "data": res_data}

    return response

# Handle check if file set is ready
@job_utility_api.route('/datastore/job/fileset/verify', methods=['POST'])
def verify_fileset():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id

    api_request = RequestVerifyFileset(request_id, PayloadVerifyFileset.form_payload(data))
    response = api_request.do_process()
    
    if response["status"] == "SUCCESS":
        res_data = response["data"]
        # merge response with data
        res_data.update(data)
        return {"status": "SUCCESS", "data": res_data}

    return response

@job_utility_api.route('/datastore/dataset/path/annotation', methods=['POST'])
def get_annotation_path():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id

    
    data.update({"directory": "annotations"})

    api_request = RequestGetDatasetPath(request_id, PayloadGetDatasetPath.form_payload(data))
    response = api_request.do_process()
    
    if "data" in response and response["status"] == "SUCCESS":
        res_data = response["data"]
        # merge response with data
        res_data.update(data)
        return {"status": "SUCCESS", "data": res_data}

    return response



@job_utility_api.route('/datastore/dataset/path/annotation/verify', methods=['POST'])
def verify_annotation_directories():
    data = json.loads(request.data)
    if "request_id" in data:
        request_id = data['request_id']
    elif "job_id" in data:
        request_id = data['job_id']
    else:
        request_id = g.request_id

    data.update({"data_type": "annotation"})

    api_request = RequestVerifyDirectories(request_id, PayloadVerifyDirectories.form_payload(data))
    response = api_request.do_process()
    
    if response["status"] == "SUCCESS":
        res_data = response["data"]
        # merge response with data
        res_data.update(data)
        return {"status": "SUCCESS", "data": res_data}

    return response



    

