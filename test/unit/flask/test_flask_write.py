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


class WriteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_scan(self):
        # Given
        mock_file = os.path.join(mock_events_folder, "write-policy-mock.json")
        with open(mock_file) as f:
            contents = f.read()
            mock_data = json.loads(contents)
        payload = json.dumps(mock_data)

        # When
        response = self.app.post("/write", headers={"Content-Type": "application/json"}, data=payload)
        print(json.dumps(response.json, indent=4))

        # Then
        # expected_response = {
        #     "body": {
        #         "Statement": [
        #             {
        #                 "Action": [
        #                     "s3:GetAccelerateConfiguration",
        #                     "s3:GetAnalyticsConfiguration",
        #                     "s3:GetBucketAcl",
        #                     "s3:GetBucketCORS",
        #                     "s3:GetBucketLocation",
        #                     "s3:GetBucketLogging",
        #                     "s3:GetBucketNotification",
        #                     "s3:GetBucketObjectLockConfiguration",
        #                     "s3:GetBucketPolicy",
        #                     "s3:GetBucketPolicyStatus",
        #                     "s3:GetBucketPublicAccessBlock",
        #                     "s3:GetBucketRequestPayment",
        #                     "s3:GetBucketTagging",
        #                     "s3:GetBucketVersioning",
        #                     "s3:GetBucketWebsite",
        #                     "s3:GetEncryptionConfiguration",
        #                     "s3:GetInventoryConfiguration",
        #                     "s3:GetLifecycleConfiguration",
        #                     "s3:GetMetricsConfiguration",
        #                     "s3:GetReplicationConfiguration",
        #                     "s3:ListBucketMultipartUploads",
        #                     "s3:ListBucketVersions"
        #                 ],
        #                 "Effect": "Allow",
        #                 "Resource": [
        #                     "arn:aws:s3:::mybucket"
        #                 ],
        #                 "Sid": "S3ReadBucket"
        #             }
        #         ],
        #         "Version": "2012-10-17"
        #     },
        #     "statusCode": 200
        # }
        # self.assertEqual(response.json, expected_response)
        self.assertEqual(200, response.status_code)

        policy = response.json.get("body")
        self.assertTrue(response.json.get("statusCode") == 200)
        self.assertTrue(policy['Statement'][0]['Sid'] == "S3ReadBucket")
        self.assertTrue(len(policy['Statement'][0]['Action']) > 20)
        self.assertTrue(len(policy["Statement"][0]["Resource"]) == 1)
