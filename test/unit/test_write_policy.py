import unittest
import json
from lambdas.write_policy.handler import write_policy


class TestWritePolicy(unittest.TestCase):
    def test_write_policy(self):
        this_event = {
            "mode": "crud",
            "read": [
                "arn:aws:s3:::example-org-s3-access-logs",
                "arn:aws:s3:::mybucket"
            ]
        }
        result = write_policy(this_event, "test")
        policy = json.loads(result.get("body"))
        print(result)
        print(policy)
        self.assertTrue(result.get("statusCode") == 200)
        self.assertTrue(policy['Statement'][0]['Sid'] == "S3ReadBucket")
        self.assertTrue(len(policy['Statement'][0]['Action']) > 20)
