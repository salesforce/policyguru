import json
import logging
from urllib.parse import parse_qs, unquote
try:
    import unzip_requirements
except ImportError:
    pass
from policy_sentry.command.write_policy import write_policy_with_template

logger = logging.getLogger()


def write_crud_policy(event, context):
    request_data = json.loads(event.get("body"))

    crud_template = {
        "mode": "crud",
    }
    if "read" in request_data:
        crud_template["read"] = request_data.get("read")
    if "write" in request_data:
        crud_template["write"] = request_data.get("write")
    if "list" in request_data:
        crud_template["list"] = request_data.get("list")
    if "tagging" in request_data:
        crud_template["tagging"] = request_data.get("tagging")
    if "permissions-management" in request_data:
        crud_template["permissions-management"] = request_data.get(
            "permissions-management")

    # Wildcard only section
    crud_template["wildcard-only"] = {}
    if "service-read" in request_data:
        crud_template["wildcard-only"]["service-read"] = request_data.get(
            "service-read"
        )
    if "service-write" in request_data:
        crud_template["wildcard-only"]["service-write"] = request_data.get(
            "service-write"
        )
    if "service-list" in request_data:
        crud_template["wildcard-only"]["service-list"] = request_data.get(
            "service-list"
        )
    if "service-tagging" in request_data:
        crud_template["wildcard-only"]["service-tagging"] = request_data.get(
            "service-tagging"
        )
    if "service-permissions-management" in request_data:
        crud_template["wildcard-only"][
            "service-permissions-management"
        ] = request_data.get("service-permissions-management")
    if "single-actions" in request_data:
        crud_template["wildcard-only"]["single-actions"] = request_data.get(
            "single-actions"
        )

    if "exclude-actions" in request_data:
        crud_template["exclude-actions"] = request_data.get("exclude-actions")

    if "skip-resource-constraints" in request_data:
        crud_template["skip-resource-constraints"] = request_data.get(
            "skip-resource-constraints"
        )

    output = write_policy_with_template(crud_template)
    # logger.info(output)
    return output


def lambda_handler(event, context):
    # TODO: Validate request data
    body = write_crud_policy(event, context)

    response = {"statusCode": 200, "body": json.dumps(body)}
    # print(json.dumps(body, indent=4))
    # TODO: output more useful log details
    # print(body)
    return response


def ui_response_handler(event, context):
    event = event['body']
    print("performing decode, event value is",event)
    event = parse_qs(event)
    print(event)
    output_data = {'mode': 'crud', 'name': '', 'read': [],
                   'write': [],
                   'list': [],
                   'tagging': [],
                   'permissions-management': [],
                   'wildcard-only': {'single-actions': [], 'service-read': [], 'service-write': [],
                                     'service-list': [], 'service-tagging': [],
                                     'service-permissions-management': []}}
    for key, val in event.items():
        indx = key.split('_')[-1]
        if 'arn' in key:
            if key.startswith('action'):
                action_name = event['action_name_'+indx][0]
                update_data = output_data
            else:
                action_name = event['wc_name_'+indx][0]
                update_data = output_data['wildcard-only']
            val = list(map(lambda x:x.strip(), unquote(val[0]).split(',')))
            update_data[action_name].extend(val)

    print("output data", output_data)

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials' : True,
            'Access-Control-Allow-Methods': 'POST,GET',
            'Content-Type': 'application/json'
        },
        "body": json.dumps(write_policy_with_template(output_data))
    }


if __name__ == "__main__":
    payload = {
        "mode": "crud",
        "read": [
            "arn:aws:s3:::mybucket"
        ]
    }
    this_event = {"body": json.dumps(payload)}
    # this_event = {"body": payload}
    this_response = lambda_handler(this_event, "test")
    print("This is a demo")
    print(this_response)
