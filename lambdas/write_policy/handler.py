import json
import logging
try:
  import unzip_requirements
except ImportError:
  pass
from policy_sentry.command.write_policy import write_policy_with_template
logger = logging.getLogger()


def write_crud_policy(request_data):
    crud_template = {
        'mode': "crud",
    }
    if "read" in request_data:
        crud_template['read'] = request_data.get('read')
    if 'write' in request_data:
        crud_template['write'] = request_data.get('write')
    if 'list' in request_data:
        crud_template['list'] = request_data.get('list')
    if 'tagging' in request_data:
        crud_template['tagging'] = request_data.get('tagging')
    if 'permissions-management' in request_data:
        crud_template['permissions-management'] = request_data.get('permissions-management')

    # Wildcard only section
    crud_template['wildcard-only'] = {}
    if 'service-read' in request_data:
        crud_template['wildcard-only']['service-read'] = request_data.get('service-read')
    if 'service-write' in request_data:
        crud_template['wildcard-only']['service-write'] = request_data.get('service-write')
    if 'service-list' in request_data:
        crud_template['wildcard-only']['service-list'] = request_data.get('service-list')
    if 'service-tagging' in request_data:
        crud_template['wildcard-only']['service-tagging'] = request_data.get('service-tagging')
    if 'service-permissions-management' in request_data:
        crud_template['wildcard-only']['service-permissions-management'] = request_data.get('service-permissions-management')
    if 'single-actions' in request_data:
        crud_template['wildcard-only']['single-actions'] = request_data.get('single-actions')

    if 'exclude-actions' in request_data:
        crud_template['exclude-actions'] = request_data.get('exclude-actions')

    if 'skip-resource-constraints' in request_data:
        crud_template['skip-resource-constraints'] = request_data.get('skip-resource-constraints')

    output = write_policy_with_template(crud_template)
    logger.info(output)
    return output


def write_policy(event, context):
    # TODO: Validate request data
    request_data = {
        "mode": "crud",
        "read": [
            "arn:aws:s3:::example-org-s3-access-logs",
            "arn:aws:s3:::mybucket"
        ]
    }
    body = write_crud_policy(request_data)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    # print(json.dumps(body, indent=4))
    # TODO: output more useful log details
    # print(body)
    return response


if __name__ == '__main__':
    this_event = {
        "mode": "crud",
        "read": [
            "arn:aws:s3:::example-org-s3-access-logs",
            "arn:aws:s3:::mybucket"
        ]
    }
    write_policy(this_event, "test")
