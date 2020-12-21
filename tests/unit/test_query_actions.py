import unittest
import json
import os
from lambdas.query_actions.app import lambda_handler
from lambdas.local_app import app

mock_events_folder = os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    os.path.pardir,
    "events",
)


class TestQueryActions(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_query_actions(self):
        this_event = {
            "queryStringParameters": {
                "service": "s3",
                "name": "GetObject",
            }
        }
        response = lambda_handler(this_event, "test")
        self.assertTrue(response.get("statusCode") == 200)
        result = json.loads(response.get("body"))
        self.assertTrue(len(result['s3']) == 2)
        for action_entry in result["s3"]:
            self.assertTrue(action_entry.get("access_level") == "Read")
            self.assertTrue(action_entry.get("action") == "s3:GetObject")

    def test_query_actions_mock(self):
        mock_filename = "query-actions-mock.json"
        mock_filepath = os.path.abspath(os.path.join(
                os.path.dirname(__file__), os.path.pardir, os.path.pardir, "events", mock_filename))
        with open(mock_filepath) as json_file:
            mock_event = json.load(json_file)

        response = lambda_handler(mock_event, "test")
        print(response)
        result = json.loads(response.get("body"))
        self.assertTrue(len(result['s3']) == 2)
        for action_entry in result["s3"]:
            self.assertTrue(action_entry.get("access_level") == "Read")
            self.assertTrue(action_entry.get("action") == "s3:GetObject")

    def test_query_actions_flask(self):
        # When
        response = self.app.get("/query/actions?service=s3&name=GetObject", headers={"Content-Type": "application/json"})
        response = response.json
        # print(json.dumps(response, indent=4))
        result = json.loads(response.get("body"))
        self.assertTrue(len(result['s3']) == 2)
        for action_entry in result["s3"]:
            self.assertTrue(action_entry.get("access_level") == "Read")
            self.assertTrue(action_entry.get("action") == "s3:GetObject")
