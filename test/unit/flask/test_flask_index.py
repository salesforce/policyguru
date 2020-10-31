import unittest

import json
from lambdas.local_app import app


class IndexTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        # Given
        payload = json.dumps({
        })

        # When
        response = self.app.get("/", headers={"Content-Type": "application/json"}, data=payload)

        # Then
        expected_response = {'hello': 'world'}
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json, expected_response)

    def test_404(self):
        # Given
        payload = json.dumps({
        })

        # When
        response = self.app.get("/yolo", headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(404, response.status_code)
