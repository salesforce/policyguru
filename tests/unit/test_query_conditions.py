import unittest
import json
import os
from lambdas.query_conditions.app import lambda_handler
from lambdas.local_app import app

mock_events_folder = os.path.join(
    os.path.dirname(__file__),
    os.path.pardir,
    os.path.pardir,
    "events",
)


class TestQueryConditions(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_query_conditions(self):
        this_event = {
            "queryStringParameters": {
                "service": "secretsmanager",
                # "name": ""
            }

        }
        response = lambda_handler(this_event, "test")
        self.assertTrue(response.get("statusCode") == 200)
        result = json.loads(response.get("body"))
        print(json.dumps(result, indent=4))
        self.assertTrue(len(result) > 13)
        # Ensure that the content of the results contains one of the expected values
        self.assertTrue("secretsmanager:KmsKeyId" in result)
        """
        [
            "aws:RequestTag/tag-key",
            "aws:TagKeys",
            "secretsmanager:BlockPublicPolicy",
            "secretsmanager:Description",
            "secretsmanager:ForceDeleteWithoutRecovery",
            "secretsmanager:KmsKeyId",
            "secretsmanager:Name",
            "secretsmanager:RecoveryWindowInDays",
            "secretsmanager:ResourceTag/tag-key",
            "secretsmanager:RotationLambdaARN",
            "secretsmanager:SecretId",
            "secretsmanager:VersionId",
            "secretsmanager:VersionStage",
            "secretsmanager:resource/AllowRotationLambdaArn"
        ]
        """

    def test_query_conditions_mock_file(self):
        mock_filename = "query-conditions-mock.json"
        mock_filepath = os.path.abspath(os.path.join(
                os.path.dirname(__file__), os.path.pardir, os.path.pardir, "events", mock_filename))
        with open(mock_filepath) as json_file:
            mock_event = json.load(json_file)

        response = lambda_handler(mock_event, "test")
        self.assertTrue(response.get("statusCode") == 200)
        result = json.loads(response.get("body"))
        print(json.dumps(result, indent=4))
        self.assertTrue(len(result) > 13)
        # Ensure that the content of the results contains one of the expected values
        self.assertTrue("secretsmanager:KmsKeyId" in result)

    def test_query_conditions_flask(self):
        # When
        response = self.app.get("/query/conditions?service=secretsmanager")
        assert (response is not None, response)
        response = response.json
        # print(json.dumps(response, indent=4))
        result = json.loads(response.get("body"))
        print(json.dumps(result, indent=4))
        self.assertTrue(len(result) > 13)
        # Ensure that the content of the results contains one of the expected values
        self.assertTrue("secretsmanager:KmsKeyId" in result)
