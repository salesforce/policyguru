import unittest
import json
import os
from lambdas.local_app import app

mock_events_folder = os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    os.path.pardir,
    os.path.pardir,
    "events",
)


class ScanTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_scan(self):
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
