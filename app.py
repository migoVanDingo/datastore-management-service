import uuid
from flask import Flask, g, jsonify, request, make_response
from flask_cors import CORS
import logging
from api.dataset.dataset_api import dataset_api
from api.dataset_roles.dataset_role_api import dataset_role_api
from api.datastore.datastore_api import datastore_api
from api.datastore_config.datastore_config_api import datastore_config_api
from api.datastore_roles.datastore_role_api import datastore_role_api
from api.files.files_api import files_api
from api.utility.job_utility_api import job_utility_api
from api.utility.utility_api import utility_api
from utility.error import ThrowError



logging.basicConfig(filename='record.log',
                level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(lineno)d | \n %(message)-20s')

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://localhost:5017"])

    #Register blueprints
    app.register_blueprint(datastore_api, url_prefix='/api')
    app.register_blueprint(dataset_api, url_prefix='/api')
    app.register_blueprint(files_api, url_prefix='/api')
    app.register_blueprint(datastore_role_api, url_prefix='/api')
    app.register_blueprint(dataset_role_api, url_prefix='/api')
    app.register_blueprint(utility_api, url_prefix='/api')
    app.register_blueprint(datastore_config_api, url_prefix='/api')
    app.register_blueprint(job_utility_api, url_prefix='/api')

    return app

app = create_app()


@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response('', 200)
        response.headers['Access-Control-Allow-Origin'] = "http://localhost:5173"
        response.headers['Access-Control-Allow-Methods'] = "POST, GET, OPTIONS, DELETE, PUT"
        response.headers['Access-Control-Allow-Headers'] = "Content-Type, Authorization"
        response.headers['Access-Control-Allow-Credentials'] = "true"
        return response
    else:
        request_id = str(uuid.uuid4())
        g.request_id = request_id


@app.errorhandler(ThrowError)
def handle_throw_error(error):
    response = jsonify({
        "message": str(error),
        "error_code": error.status_code
    })
    response.status_code = error.status_code
    return response