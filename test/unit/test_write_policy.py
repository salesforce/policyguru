import unittest
import os
import json
from lambdas.write_policy.handler import write_policy


class TestWritePolicy(unittest.TestCase):
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
        response = write_policy(this_event, "test")
        # policy = json.loads(response.get("body"))
        policy = response.get("body")
        self.assertTrue(response.get("statusCode") == 200)
        print(response)
        self.assertTrue(policy['Statement'][0]['Sid'] == "S3ReadBucket")
        self.assertTrue(len(policy['Statement'][0]['Action']) > 20)
        self.assertTrue(len(policy["Statement"][0]["Resource"]) == 1)

    def test_write_policy_mock(self):
        mock_filename = "write-policy-mock.json"
        mock_filepath = os.path.abspath(os.path.join(
                os.path.dirname(__file__), os.path.pardir, os.path.pardir, "events", mock_filename))
        with open(mock_filepath) as json_file:
            mock_event = json.load(json_file)

        response = write_policy(mock_event, "test")
        # policy = json.loads(response.get("body"))
        policy = response.get("body")
        self.assertTrue(response.get("statusCode") == 200)
        self.assertTrue(policy['Statement'][0]['Sid'] == "S3ReadBucket")
        self.assertTrue(len(policy['Statement'][0]['Action']) > 20)
        self.assertTrue(len(policy["Statement"][0]["Resource"]) == 1)
