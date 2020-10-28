import unittest
import json
import os
from lambdas.query_conditions.handler import query_conditions


class TestQueryConditions(unittest.TestCase):
    def test_query_conditions(self):
        this_event = {
            "queryStringParameters": {
                "service": "secretsmanager",
                # "name": ""
            }

        }
        response = query_conditions(this_event, "test")
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

        response = query_conditions(mock_event, "test")
        self.assertTrue(response.get("statusCode") == 200)
        result = json.loads(response.get("body"))
        print(json.dumps(result, indent=4))
        self.assertTrue(len(result) > 13)
        # Ensure that the content of the results contains one of the expected values
        self.assertTrue("secretsmanager:KmsKeyId" in result)
