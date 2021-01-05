import unittest
import os
import json
from lambdas.write_policy.app import lambda_handler
# from lambdas.local_app import app

mock_events_folder = os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    os.path.pardir,
    "events",
)


class TestWritePolicy(unittest.TestCase):
    # def setUp(self):
    #     self.app = app.test_client()

    def test_write_policy(self):
        this_event = {
            "body": json.dumps({
                "mode": "crud",
                "read": [
                    "arn:aws:s3:::example-org-s3-access-logs",
                ]
            })
        }
        # this_event = {"body": json.dumps(payload)}
        response = lambda_handler(this_event, "test")
        # policy = json.loads(response.get("body"))
        policy = json.loads(response.get("body"))
        self.assertTrue(response.get("statusCode") == 200)
        print(response)
        self.assertTrue(policy['Statement'][0]['Sid'] == "S3ReadBucket")
        self.assertTrue(len(policy['Statement'][0]['Action']) > 20)
        self.assertTrue(len(policy["Statement"][0]["Resource"]) == 1)

    def test_write_policy_mock(self):
        mock_file = os.path.join(mock_events_folder, "write-policy-mock.json")
        with open(mock_file) as f:
            mock_data = json.load(f)

        response = lambda_handler(mock_data, "test")
        # policy = json.loads(response.get("body"))
        policy = json.loads(response.get("body"))
        self.assertTrue(response.get("statusCode") == 200)
        self.assertTrue(policy['Statement'][0]['Sid'] == "S3ReadBucket")
        self.assertTrue(len(policy['Statement'][0]['Action']) > 20)
        self.assertTrue(len(policy["Statement"][0]["Resource"]) == 1)

    # def test_write_flask(self):
    #     # api gateway's request and response object is different than flask's request and response object
    #     # so the tests for flask have different request/response
    #     # Given
    #     mock_file = os.path.join(mock_events_folder, "write-policy-mock.json")
    #     with open(mock_file) as f:
    #         contents = f.read()
    #         mock_data = json.loads(contents)
    #     payload_body = json.loads(mock_data["body"])
    #
    #     # When
    #     response = self.app.post("/write", headers={"Content-Type": "application/json"}, data=json.dumps(payload_body))
    #     print(json.dumps(response.json, indent=4))
    #     self.assertEqual(200, response.status_code)
    #
    #     policy = response.json
    #     self.assertTrue(policy['Statement'][0]['Sid'] == "S3ReadBucket")
    #     self.assertTrue(len(policy['Statement'][0]['Action']) > 20)
    #     self.assertTrue(len(policy["Statement"][0]["Resource"]) == 1)
