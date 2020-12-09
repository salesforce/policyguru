#!/usr/bin/env python

import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_swagger import swagger
from lambdas.scan_policy.app import lambda_handler as cloudsplaining_scan_policy
from lambdas.write_policy.app import lambda_handler as write_policy
from lambdas.query_actions.app import lambda_handler as query_actions
from lambdas.query_resources.app import lambda_handler as query_resources
from lambdas.query_conditions.app import lambda_handler as query_conditions

app = Flask(__name__)
logger = logging.getLogger()


@app.route('/')
def home():
    return {'hello': 'world'}


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/scan', methods=['POST'])
def scan_lambda():
    request_data = request.get_json()
    response = cloudsplaining_scan_policy(request_data, "localTest")
    logger.info(response)
    return jsonify(response)


@app.route('/write', methods=['POST'])
def write_lambda():
    request_data = request.get_json()
    response = write_policy(request_data, "localTest")
    logger.info(response)
    return jsonify(response)


@app.route('/query/actions', methods=['GET'])
def query_actions_lambda():
    request_data = request.get_json()
    response = query_actions(request_data, "localTest")
    logger.info(response)
    return jsonify(response)


@app.route('/query/resources', methods=['GET'])
def query_resources_lambda():
    request_data = request.get_json()
    response = query_resources(request_data, "localTest")
    logger.info(response)
    return jsonify(response)


@app.route('/query/conditions', methods=['GET'])
def query_conditions_lambda():
    request_data = request.get_json()
    response = query_conditions(request_data, "localTest")
    logger.info(response)
    return jsonify(response)


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "0.0.1"
    swag['info']['title'] = "Policy Sentry API"
    return jsonify(swag)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # nosec
