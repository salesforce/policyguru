import json
import logging
from policy_sentry.command.query import query_condition_table
try:
    import unzip_requirements
except ImportError:
    pass

logger = logging.getLogger()


def query_conditions(event, context):
    # TODO: Validate request data
    service = (event["queryStringParameters"]).get('service')
    name = event["queryStringParameters"].get('name', None)

    body = query_condition_table(name, service)

    response = {"statusCode": 200, "body": json.dumps(body)}
    # print(json.dumps(body, indent=4))
    # print(body)
    return response


if __name__ == "__main__":
    this_event = {
        # "name": "",
        "service":  "s3",
    }

    query_conditions(this_event, "test")
