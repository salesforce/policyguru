import json
import logging
from policy_sentry.command.query import query_action_table
try:
    import unzip_requirements
except ImportError:
    pass

logger = logging.getLogger()


def query_actions(event, context):
    # TODO: Validate request data
    service = event.get('service')
    name = event.get('name', None)
    access_level = event.get('access_level', None)
    condition = event.get('condition', None)
    resource_type = event.get('resource_type', None)

    body = query_action_table(name, service, access_level, condition, resource_type)

    response = {"statusCode": 200, "body": json.dumps(body)}
    # print(json.dumps(body, indent=4))
    # print(body)
    return response


if __name__ == "__main__":
    this_event = {
        "name": "GetObject",
        "service":  "s3",
        # "access_level": "",
        # "condition": ""
        # "resource_type": "",
    }

    query_actions(this_event, "test")
