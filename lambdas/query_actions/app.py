import json
import logging
from policy_sentry.command.query import query_action_table

try:
    import unzip_requirements
except ImportError:
    pass

logger = logging.getLogger()


def lambda_handler(event, context):
    # TODO: Validate request data
    service = (event["queryStringParameters"]).get('service')
    name = event["queryStringParameters"].get('name', None)
    access_level = event["queryStringParameters"].get('access_level', None)
    condition = event["queryStringParameters"].get('condition', None)
    resource_type = event["queryStringParameters"].get('resource_type', None)

    body = query_action_table(name, service, access_level, condition, resource_type)

    response = {"statusCode": 200, "body": json.dumps(body)}
    # print(json.dumps(body, indent=4))
    # print(body)
    return response


if __name__ == "__main__":
    this_event = {
        "queryStringParameters": {
            "name": "GetObject",
            "service":  "s3",
            # "access_level": "",
            # "condition": ""
            # "resource_type": "",
        }
    }

    response = lambda_handler(this_event, "test")
    print("This is a demo")
    print(response)
