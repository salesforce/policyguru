# pylint: disable=missing-module-docstring
# TODO: NOTE THAT WE HAD TO CALL 'LIST' PARAMETER 'LIST_ACCESS' DUE TO PYTHON AND PYDANTIC THROWING VALIDATION ERRORS
import logging
from typing import Optional, List

from fastapi import APIRouter
from pydantic import BaseModel, Field
import copy
from policy_sentry.command.write_policy import write_policy_with_template
logger = logging.getLogger()

router = APIRouter()


class ActionsForResourcesAtAccessLevel(BaseModel):
    read: Optional[List] = Field(
        title="'Read' access level to ARNs",
        description="Grant 'Read' level access to these Resource ARNs.",
        default=[]
    )
    write: Optional[List] = Field(
        title="'Write' access level to ARNs",
        description="Grant 'Write' level access to these Resource ARNs.",
        default=[]
    )
    permissions_management: Optional[List] = Field(
        title="'Permissions management' access level to ARNs",
        description="Grant 'Permissions management' level access to these Resource ARNs.",
        default=[]
    )
    tagging: Optional[List] = Field(
        title="'Tagging' access level to ARNs",
        description="Grant 'Tagging' level access to these Resource ARNs.",
        default=[]
    )
    list_access: Optional[List] = Field(
        title="'List' access level to ARNs",
        description="Grant 'List' level access to these Resource ARNs.",
        default=[]
    )


class ActionsForServicesWithoutResourceConstraintSupport(BaseModel):
    single_actions: Optional[List] = Field(
        title="Individual actions that do not support resource ARN constraints",
        description="Individual actions that do not support resource ARN constraints",
        default=[]
    )
    read: Optional[List] = Field(
        title="'Read' level actions for actions that do **not** support resource ARN constraints",
        description="'Read' level actions for actions that do **not** support resource ARN constraints",
        default=[]
    )
    write: Optional[List] = Field(
        title="Write level actions for actions that do **not** support resource ARN constraints",
        description="'Write' level actions for actions that do **not** support resource ARN constraints",
        default=[]
    )
    permissions_management: Optional[List] = Field(
        title="Permissions management level actions for actions that do **not** support resource ARN constraints",
        description="'Permissions management' level actions for actions that do **not** support resource ARN "
                    "constraints",
        default=[]
    )
    tagging: Optional[List] = Field(
        title="'Tagging' level actions for actions that do **not** support resource ARN constraints",
        description="'Tagging' level actions for actions that do **not** support resource ARN constraints",
        default=[]
    )
    list_access: Optional[List] = Field(
        title="List level actions for actions that do **not** support resource ARN constraints",
        description="'List' level actions for actions that do **not** support resource ARN constraints",
        default=[]
    )


default_actions_for_resources_at_access_level = ActionsForResourcesAtAccessLevel(
    read=[],
    write=[],
    list_access=[],
    tagging=[],
    permissions_management=[],
)

default_actions_for_services_without_resource_constraint_support = ActionsForServicesWithoutResourceConstraintSupport(
    single_actions=[],
    read=[],
    write=[],
    list_access=[],
    tagging=[],
    permissions_management=[],
)


class WritePolicyInput(BaseModel):
    name: str
    actions_for_resources_at_access_level: Optional[ActionsForResourcesAtAccessLevel] = Field(
        default=default_actions_for_resources_at_access_level,
        title="Resource ARNs at Access Level",
        description="Supply Resource ARNs here under the requested access levels. This will return actions that are "
                    "restricted to those resource ARNs and access level only."
    )
    actions_for_services_without_resource_constraint_support: Optional[ActionsForServicesWithoutResourceConstraintSupport] = Field(
        default=default_actions_for_services_without_resource_constraint_support,
        title="Actions for Services without Resource Constraint Support",
        description="Some AWS Actions do not support resource ARN constraints, and thus require the use of '*' . To "
                    "get those actions, list the service and access level here. "
    )

    # Override sections
    skip_resource_constraints: Optional[List] = Field(
        title="Skip Resource Constraints for Actions",
        description="Skip resource constraint requirements by listing actions here.",
        default=[]
    )
    exclude_actions: Optional[List] = Field(
        title="Exclude Actions",
        description="Exclude actions from the output by specifying them here. Accepts wildcards, like 'kms:Delete*'",
        default=[]
    )


class WritePolicyResponse(BaseModel):
    Version: str = Field(
        title="Version",
        description="Version of the Policy Language. Must be 2012-10-17",
        default="2012-10-17"
    )
    Statement: list = Field(
        title="Statement",
        description="The Statement Block contains a list of IAM statements.",
        default=[]
    )


class WritePolicyTemplate:
    def __init__(self, write_policy_input):
        if not isinstance(write_policy_input, WritePolicyInput):
            raise Exception("Please supply a WritePolicyInput BaseModel object.")
        self.name = write_policy_input.name
        self.read = write_policy_input.actions_for_resources_at_access_level.read
        self.write = write_policy_input.actions_for_resources_at_access_level.write
        self.list = write_policy_input.actions_for_resources_at_access_level.list_access
        self.tagging = write_policy_input.actions_for_resources_at_access_level.tagging
        self.permissions_management = write_policy_input.actions_for_resources_at_access_level.permissions_management

        # print(write_policy_input.actions_for_services_without_resource_constraint_support['single-actions'])
        this_wildcard_only = write_policy_input.actions_for_services_without_resource_constraint_support

        self.wildcard_only = {
            "single-actions": this_wildcard_only.single_actions,
            "service-read": this_wildcard_only.read,
            "service-write": this_wildcard_only.write,
            "service-list": this_wildcard_only.list_access,
            "service-tagging": this_wildcard_only.tagging,
            "service-permissions-management": this_wildcard_only.permissions_management,
        }
        self.exclude_actions = write_policy_input.exclude_actions
        self.skip_resource_constraints = write_policy_input.skip_resource_constraints

    @property
    def json(self):
        crud_template = {
            "name": self.name,
            "mode": "crud",
            "read": self.read,
            "write": self.write,
            "list": self.list,
            "tagging": self.tagging,
            "permissions-management": self.permissions_management,
            "wildcard-only": self.wildcard_only,
            "skip-resource-constraints": self.skip_resource_constraints,
            "exclude-actions": self.exclude_actions
        }
        return crud_template


@router.post("/write-iam-policy", response_model=WritePolicyResponse)
async def write_iam_policy(
    item: WritePolicyInput
):
    template = WritePolicyTemplate(item)
    output = write_policy_with_template(template.json)
    return output
