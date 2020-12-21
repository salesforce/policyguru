#!/usr/bin/env python

import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_swagger import swagger
from flask import Response
from lambdas.scan_policy.app import lambda_handler as cloudsplaining_scan_policy
from lambdas.write_policy.app import lambda_handler as write_policy
from lambdas.query_actions.app import lambda_handler as query_actions
from lambdas.query_resources.app import lambda_handler as query_resources
from lambdas.query_conditions.app import lambda_handler as query_conditions

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


@app.route('/')
def home():
    return {'hello': 'world'}


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/scan', methods=['POST'])
def scan_lambda():
    # do not change the request_data and response, it will break integration lambda
    request_data = {}
    request_data["body"] = json.dumps(request.get_json())
    response = cloudsplaining_scan_policy(request_data, "localTest")
    logger.info(response)
    return Response(response["body"], status=200, mimetype='application/json')


# Only added "Get" so you can run Terraform provider locally
@app.route('/write', methods=['POST'])
def write_lambda():
    # do not change the request_data and response, it will break integration lambda
    request_data = {}
    request_data["body"] = json.dumps(request.get_json())
    response = write_policy(request_data, "localTest")
    logger.info(response)
    return Response(response["body"], status=200, mimetype='application/json')

@app.route('/query/actions', methods=['GET'])
def query_actions_lambda():
    # do not change the request_data and response, it will break integration lambda
    request_data = {}
    request_data["queryStringParameters"] = request.args
    logger.info(request_data)
    response = query_actions(request_data, "localTest")
    logger.info(response)
    return jsonify(response)


@app.route('/query/resources', methods=['GET'])
def query_resources_lambda():
    # do not change the request_data and response, it will break integration lambda
    request_data = {}
    request_data["queryStringParameters"] = request.args
    response = query_resources(request_data, "localTest")
    logger.info(response)
    return jsonify(response)


@app.route('/query/conditions', methods=['GET'])
def query_conditions_lambda():
    # do not change the request_data and response, it will break integration lambda
    request_data = {}
    request_data["queryStringParameters"] = request.args
    response = query_conditions(request_data, "localTest")
    print (response)
    return jsonify(response)


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "0.0.1"
    swag['info']['title'] = "Policy Sentry API"
    return jsonify(swag)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # nosec
