import json
import logging
from cloudsplaining.command.scan_policy_file import scan_policy

try:
    import unzip_requirements
except ImportError:
    pass

logger = logging.getLogger()


def cloudsplaining_scan_policy(event, context):
    request_data = json.loads(event.get("body"))
    policy_document = request_data.get('policy_document')
    include_actions = request_data.get('include_actions')
    exclude_actions = request_data.get('exclude_actions')

    # If include_actions is not included in the request, then just give it the default values.
    if not include_actions:
        include_actions = [
            "s3:GetObject",
            "ssm:GetParameter",
            "ssm:GetParameters",
            "ssm:GetParametersByPath",
            "secretsmanager:GetSecretValue",
            "rds:CopyDBSnapshot",
            "rds:CreateDBSnapshot"
        ]
    if not exclude_actions:
        exclude_actions = []

    exclusions_cfg = {
        "exclude-actions": exclude_actions,
        "include-actions": include_actions
    }
    body = scan_policy(policy_document, exclusions_cfg)

    response = {"statusCode": 200, "body": json.dumps(body)}
    return response


if __name__ == "__main__":
    this_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                ],
                "Resource": "*",
            }
        ]
    }
    payload = {
        "policy_document": this_policy_document,
        "include_actions": [
            "s3:GetObject",
            "ssm:GetParameter",
            "ssm:GetParameters",
            "ssm:GetParametersByPath",
            "secretsmanager:GetSecretValue",
            "rds:CopyDBSnapshot",
            "rds:CreateDBSnapshot"
        ],
        "exclude_actions": []
    }
    # this_event = {"body": json.dumps(payload)}
    this_event = {"body": payload}

    response = cloudsplaining_scan_policy(this_event, "test")
    print("this is a demo")
    print(response)
