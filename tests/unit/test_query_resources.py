import unittest
import os
import json
from lambdas.query_resources.app import lambda_handler
from lambdas.local_app import app

mock_events_folder = os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    os.path.pardir,
    "events",
)


class TestQueryResources(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_query_resources(self):
        this_event = {
            "queryStringParameters": {
                "service": "s3",
                "list_arn_types": True,
            }
        }
        response = lambda_handler(this_event, "test")
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

    def test_query_resources_mock_file(self):
        mock_filename = "query-resources-mock.json"
        mock_filepath = os.path.abspath(os.path.join(
                os.path.dirname(__file__), os.path.pardir, os.path.pardir, "events", mock_filename))
        with open(mock_filepath) as json_file:
            mock_event = json.load(json_file)

        response = lambda_handler(mock_event, "test")
        self.assertTrue(response.get("statusCode") == 200)
        result = json.loads(response.get("body"))
        for arn_type in ["accesspoint", "bucket", "object", "job"]:
            self.assertTrue(result.get(arn_type))

    def test_query_resources_flask(self):
        # When
        response = self.app.get("/query/resources?service=s3&list_arn_types=true", headers={"Content-Type": "application/json"})
        response = response.json
        # print(json.dumps(response, indent=4))
        result = json.loads(response.get("body"))
        for arn_type in ["accesspoint", "bucket", "object", "job"]:
            self.assertTrue(result.get(arn_type))
