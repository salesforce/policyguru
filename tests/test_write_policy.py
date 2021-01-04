import unittest
import json
from starlette.testclient import TestClient
from policy_sentry.util.policy_files import get_sid_names_from_policy
from policy_sentry.command.write_policy import write_policy_with_template
from app.api.write_iam_policy import WritePolicyInput, WritePolicyTemplate, ActionsForServicesWithoutResourceConstraintSupport, ActionsForResourcesAtAccessLevel
from app.main import app

client = TestClient(app)


class TestWritePolicy(unittest.TestCase):
    def test_schema_actions_for_services_without_resource_constraint_support(self):
        wildcard_only_section = ActionsForServicesWithoutResourceConstraintSupport(
            read=[],
            write=[],
            list_access=[],
            permissions_management=[],
            tagging=[],
            single_actions=["s3:ListAllMyBuckets"]
        )
        result = wildcard_only_section.dict()
        # print(json.dumps(stuff.dict(), indent=4))
        expected_result = {
            "single_actions": [
                "s3:ListAllMyBuckets"
            ],
            "read": [],
            "write": [],
            "permissions_management": [],
            "tagging": [],
            "list_access": []
        }
        self.assertDictEqual(result, expected_result)

    def test_schema_actions_for_resources_at_access_level(self):
        actions_for_resources_at_access_level = ActionsForResourcesAtAccessLevel(
            read=["arn:aws:s3:::mybucket/*"],
            write=[],
            list_access=[],
            permissions_management=[],
            tagging=[],
        )
        results = actions_for_resources_at_access_level.dict()
        print(json.dumps(results, indent=4))
        expected_results = {
            "read": [
                "arn:aws:s3:::mybucket/*"
            ],
            "write": [],
            "permissions_management": [],
            "tagging": [],
            "list_access": []
        }
        self.assertDictEqual(results, expected_results)

    def test_write_policy_input_schema(self):
        actions_for_resources_at_access_level = {
            "read": [],
            "write": [],
            "list": [],
            "tagging": [],
            "permissions-management": [],
        }
        actions_for_services_without_resource_constraint_support = {
            "single-actions": [],
            "read": [],
            "write": [],
            "list": [],
            "tagging": [],
            "permissions-management": [],
        }
        wildcard_only_section = ActionsForServicesWithoutResourceConstraintSupport(
            read=[],
            write=[],
            list_access=[],
            permissions_management=[],
            tagging=[],
            single_actions=["s3:ListAllMyBuckets"]
        )
        actions_for_resources_at_access_level = ActionsForResourcesAtAccessLevel(
            read=["arn:aws:s3:::mybucket/*"],
            write=[],
            list_access=[],
            permissions_management=[],
            tagging=[],
        )

        write_policy_input = WritePolicyInput(
            name="test",
            actions_for_resources_at_access_level=actions_for_resources_at_access_level,
            actions_for_services_without_resource_constraint_support=wildcard_only_section,
            skip_resource_constraints=["s3:PutObject"],
            exclude_actions=["kms:Delete*"]
        )
        template = WritePolicyTemplate(write_policy_input)
        results = write_policy_with_template(template.json)
        print(json.dumps(results, indent=4))
        expected_results = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListAllMyBuckets"
                    ],
                    "Resource": [
                        "*"
                    ]
                },
                {
                    "Sid": "S3ReadObject",
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:GetObjectAcl",
                        "s3:GetObjectLegalHold",
                        "s3:GetObjectRetention",
                        "s3:GetObjectTagging",
                        "s3:GetObjectTorrent",
                        "s3:GetObjectVersion",
                        "s3:GetObjectVersionAcl",
                        "s3:GetObjectVersionForReplication",
                        "s3:GetObjectVersionTagging",
                        "s3:GetObjectVersionTorrent"
                    ],
                    "Resource": [
                        "arn:aws:s3:::mybucket/*"
                    ]
                },
                {
                    "Sid": "SkipResourceConstraints",
                    "Effect": "Allow",
                    "Action": [
                        "s3:PutObject"
                    ],
                    "Resource": [
                        "*"
                    ]
                }
            ]
        }
        self.assertListEqual(get_sid_names_from_policy(results), get_sid_names_from_policy(expected_results))
        # self.assertDictEqual(output, expected_results)

    def test_write_iam_policy(self):
        payload = {
            "name": "test",
            "actions_for_resources_at_access_level": {
                "read": ["arn:aws:s3:::mybucket/*"]
            }
        }
        response = client.put("/write-iam-policy", json.dumps(payload))
        self.assertTrue(response.status_code == 200)
        results = response.json()
        self.assertListEqual(get_sid_names_from_policy(results), ["S3ReadObject"])
