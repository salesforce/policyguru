import unittest
import json
from lambdas.query_actions.handler import query_actions


class TestQueryActions(unittest.TestCase):
    def test_query_actions(self):
        this_event = {
            "service": "s3",
            "name": "GetObject",
        }
        response = query_actions(this_event, "test")
        self.assertTrue(response.get("statusCode") == 200)
        result = json.loads(response.get("body"))
        self.assertTrue(len(result['s3']) == 2)
        for action_entry in result["s3"]:
            self.assertTrue(action_entry.get("access_level") == "Read")
            self.assertTrue(action_entry.get("action") == "s3:GetObject")

