import unittest
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
        this_event = {
            "policy_document": this_policy_document,
        }
        response = cloudsplaining_scan_policy(this_event, "test")
        print(response)
        result = json.loads(response.get("body"))

        self.assertTrue(result["ServicesAffected"][0] == "s3")
        self.assertTrue(result["DataExfiltration"][0] == "s3:GetObject")
