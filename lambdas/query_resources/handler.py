import json
import logging
from policy_sentry.command.query import query_arn_table

try:
    import unzip_requirements
except ImportError:
    pass

logger = logging.getLogger()


def query_resources(event, context):
    # TODO: Validate request data
    service = (event["queryStringParameters"]).get('service')
    name = event["queryStringParameters"].get('name', None)
    list_arn_types = (event["queryStringParameters"]).get('list_arn_types', False)

    body = query_arn_table(name, service, list_arn_types, fmt=json)

    response = {"statusCode": 200, "body": json.dumps(body)}
    # print(json.dumps(body, indent=4))
    # print(body)
    return response


if __name__ == "__main__":
    this_event = {
        "queryStringParameters": {
            "service":  "s3",
            "list_arn_types": True,
            # "name": "",
        }
    }

    response = query_resources(this_event, "test")
    print("This is a demo")
    print(response)