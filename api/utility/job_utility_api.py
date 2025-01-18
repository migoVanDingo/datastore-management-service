from flask import Blueprint, g, request
import json

from api.datastore.handler.request_verify_fileset import RequestVerifyFileset
from api.datastore.payload.payload_verify_fileset import PayloadVerifyFileset


job_utility_api = Blueprint('job_utility_api', __name__)

# Handle check if file set is ready
@job_utility_api.route('/datastore/job/fileset/verify', methods=['POST'])
def verify_fileset():
    data = json.loads(request.data)
    request_id = data['request_id'] if 'request_id' in data else g.request_id

    api_request = RequestVerifyFileset(request_id, PayloadVerifyFileset.form_payload(data))
    response = api_request.do_process()
    
    # merge response with data
    response.update(data)
    return {"status": "SUCCESS", "data": response}


    

