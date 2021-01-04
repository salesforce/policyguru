import unittest
import json
from starlette.testclient import TestClient

from app.api.scan_iam_policy import ScanPolicyInput, ScanPolicyResponse
from app.main import app

client = TestClient(app)

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


class TestScanPolicy(unittest.TestCase):
    def test_scan_iam_policy(self):
        response = client.put("/scan-iam-policy", json.dumps(payload))
        self.assertTrue(response.status_code == 200)
        result = response.json()

        self.assertTrue(result.get("ServicesAffected") == ["s3"])
        self.assertTrue(result.get("InfrastructureModification") == ["s3:GetObject"])
        # assert response.json() == {"ping": "pong!"}

    def test_scan_policy_input_schema(self):
        include_actions = [
            "s3:GetObject",
            "ssm:GetParameter",
            "ssm:GetParameters",
            "ssm:GetParametersByPath",
            "secretsmanager:GetSecretValue",
            "rds:CopyDBSnapshot",
            "rds:CreateDBSnapshot"
        ],
        exclude_actions = []
        scan_policy_input = ScanPolicyInput(
            policy_document=this_policy_document,
            exclude_actions=exclude_actions,
            include_actions=include_actions
        )
        expected_result = {
            "policy_document": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "s3:GetObject"
                        ],
                        "Resource": "*"
                    }
                ]
            },
            "exclude_actions": [],
            "include_actions": [
                [
                    "s3:GetObject",
                    "ssm:GetParameter",
                    "ssm:GetParameters",
                    "ssm:GetParametersByPath",
                    "secretsmanager:GetSecretValue",
                    "rds:CopyDBSnapshot",
                    "rds:CreateDBSnapshot"
                ]
            ]
        }
        self.assertDictEqual(scan_policy_input.dict(), expected_result)

        # print(json.dumps(scan_policy_input.dict(), indent=4))
        # print(scan_policy_input.__fields__)
