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


class QueryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_query_actions(self):
        # Given
        mock_file = os.path.join(mock_events_folder, "query-actions-mock.json")
        with open(mock_file) as f:
            contents = f.read()
            mock_data = json.loads(contents)
        payload = json.dumps(mock_data)

        # When
        response = self.app.get("/query/actions", headers={"Content-Type": "application/json"}, data=payload)
        response = response.json
        # print(json.dumps(response, indent=4))
        result = json.loads(response.get("body"))
        self.assertTrue(len(result['s3']) == 2)
        for action_entry in result["s3"]:
            self.assertTrue(action_entry.get("access_level") == "Read")
            self.assertTrue(action_entry.get("action") == "s3:GetObject")

    def test_query_resources(self):
        # Given
        mock_file = os.path.join(mock_events_folder, "query-resources-mock.json")
        with open(mock_file) as f:
            contents = f.read()
            mock_data = json.loads(contents)
        payload = json.dumps(mock_data)

        # When
        response = self.app.get("/query/resources", headers={"Content-Type": "application/json"}, data=payload)
        response = response.json
        # print(json.dumps(response, indent=4))
        result = json.loads(response.get("body"))
        for arn_type in ["accesspoint", "bucket", "object", "job"]:
            self.assertTrue(result.get(arn_type))

    def test_query_conditions(self):
        # Given
        mock_file = os.path.join(mock_events_folder, "query-conditions-mock.json")
        with open(mock_file) as f:
            contents = f.read()
            mock_data = json.loads(contents)
        payload = json.dumps(mock_data)

        # When
        response = self.app.get("/query/conditions", headers={"Content-Type": "application/json"}, data=payload)
        response = response.json
        # print(json.dumps(response, indent=4))
        result = json.loads(response.get("body"))
        print(json.dumps(result, indent=4))
        self.assertTrue(len(result) > 13)
        # Ensure that the content of the results contains one of the expected values
        self.assertTrue("secretsmanager:KmsKeyId" in result)
