import unittest
import json
from lambdas.query_resources.handler import query_resources


class TestQueryResources(unittest.TestCase):
    def test_query_resources(self):
        this_event = {
            "queryStringParameters": {
                "service": "s3",
                "list_arn_types": True,
            }
        }
        response = query_resources(this_event, "test")
        self.assertTrue(response.get("statusCode") == 200)
        result = json.loads(response.get("body"))
        for arn_type in ["accesspoint", "bucket", "object", "job"]:
            self.assertTrue(result.get(arn_type))
        """
        {
            "accesspoint": "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
            "bucket": "arn:${Partition}:s3:::${BucketName}",
            "object": "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
            "job": "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}"
        }
        """
