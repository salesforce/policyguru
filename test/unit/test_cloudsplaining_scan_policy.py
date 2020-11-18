import unittest
import os
import json
from lambdas.cloudsplaining_scan_policy.handler import cloudsplaining_scan_policy


class TestScanPolicy(unittest.TestCase):
    def test_scan_policy(self):
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
        this_event = {"body": json.dumps(payload)}
        print(this_event)
        response = cloudsplaining_scan_policy(this_event, "test")
        print(response)
        result = json.loads(response.get("body"))
        self.assertTrue(result["ServicesAffected"][0] == "s3")
        self.assertTrue(result["DataExfiltration"][0] == "s3:GetObject")

    def test_scan_policy_mock(self):
        mock_filename = "scan-policy-mock.json"
        mock_filepath = os.path.abspath(os.path.join(
                os.path.dirname(__file__), os.path.pardir, os.path.pardir, "events", mock_filename))
        with open(mock_filepath) as json_file:
            mock_event = json.load(json_file)

        response = cloudsplaining_scan_policy(mock_event, "test")
        print(response)
        result = json.loads(response.get("body"))
        self.assertTrue(result["ServicesAffected"][0] == "s3")
        self.assertTrue(result["DataExfiltration"][0] == "s3:GetObject")
