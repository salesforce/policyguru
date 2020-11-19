import unittest
import os
import json
from lambdas.cloudsplaining_scan_policy.handler import cloudsplaining_scan_policy
from lambdas.local_app import app

mock_events_folder = os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    os.path.pardir,
    "events",
)


class TestScanPolicy(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

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

    def test_scan_flask(self):
        # Given
        mock_file = os.path.join(mock_events_folder, "scan-policy-mock.json")
        with open(mock_file) as f:
            contents = f.read()
            mock_data = json.loads(contents)
        payload = json.dumps(mock_data)

        # When
        response = self.app.post("/scan", headers={"Content-Type": "application/json"}, data=payload)
        print(json.dumps(response.json, indent=4))

        # Then
        expected_response = {
            "body": {
                "CredentialsExposure": [],
                "DataExfiltration": [
                    "s3:GetObject"
                ],
                "InfrastructureModification": [
                    "s3:GetObject"
                ],
                "PrivilegeEscalation": [],
                "ResourceExposure": [],
                "ServiceWildcard": [],
                "ServicesAffected": [
                    "s3"
                ]
            },
            "statusCode": 200
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, expected_response)
