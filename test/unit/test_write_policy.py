import unittest
import json
from lambdas.write_policy.handler import write_policy


class TestWritePolicy(unittest.TestCase):
    def test_write_policy(self):
        payload = {
            "mode": "crud",
            "read": [
                "arn:aws:s3:::example-org-s3-access-logs",
            ]
        }
        this_event = {"body": json.dumps(payload)}
        response = write_policy(this_event, "test")
        policy = json.loads(response.get("body"))
        self.assertTrue(response.get("statusCode") == 200)
        self.assertTrue(policy['Statement'][0]['Sid'] == "S3ReadBucket")
        self.assertTrue(len(policy['Statement'][0]['Action']) > 20)
        self.assertTrue(len(policy["Statement"][0]["Resource"]) == 1)
