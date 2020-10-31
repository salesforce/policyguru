import unittest
import json
import os
from lambdas.query_actions.handler import query_actions
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
        response = query_actions(this_event, "test")
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

        response = query_actions(mock_event, "test")
        print(response)
        result = json.loads(response.get("body"))
        self.assertTrue(len(result['s3']) == 2)
        for action_entry in result["s3"]:
            self.assertTrue(action_entry.get("access_level") == "Read")
            self.assertTrue(action_entry.get("action") == "s3:GetObject")

    def test_query_actions_flask(self):
        # Given
        mock_file = os.path.join(mock_events_folder, "query-actions-mock.json")
        with open(mock_file) as f:
            mock_data = json.load(f)
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
