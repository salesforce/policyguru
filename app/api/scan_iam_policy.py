# pylint: disable=missing-module-docstring
import logging
from typing import Optional, List

from fastapi import APIRouter
from pydantic import BaseModel, Field

from cloudsplaining.command.scan_policy_file import scan_policy as scan_policy

logger = logging.getLogger()

router = APIRouter()

INCLUDE_ACTIONS_DEFAULT = [
    "s3:GetObject",
    "ssm:GetParameter",
    "ssm:GetParameters",
    "ssm:GetParametersByPath",
    "secretsmanager:GetSecretValue",
    "rds:CopyDBSnapshot",
    "rds:CreateDBSnapshot"
]

EXCLUDE_ACTIONS_DEFAULT = []


class ScanPolicyInput(BaseModel):
    policy_document: dict = Field(
        title="Policy Document",
        description="The JSON of the valid AWS IAM Policy Document."
    )
    exclude_actions = Field(
        title="Actions to Exclude",
        description="IAM Actions to Exclude from evaluation",
        default=EXCLUDE_ACTIONS_DEFAULT
    )
    include_actions = Field(
        title="Actions to Always Include.",
        description="IAM Actions to always include in evaluation. Typically used for 'read/list' level actions that "
                    "you want to include, instead of just write level actions.",
        default=INCLUDE_ACTIONS_DEFAULT
    )


class ScanPolicyResponse(BaseModel):
    ServicesAffected: List[str] = Field(
        title="AWS Services Affected",
        description="AWS services affected by these findings.",
        default=None
    )
    ServiceWildcard: List[str] = Field(
        title="Service Wildcard Findings",
        description="The IAM Policy allows ALL actions under these services - like when `s3:*` is in the policy.",
        default=None
    )
    PrivilegeEscalation: List[str] = Field(
        title="Privilege Escalation Findings",
        description="Combinations of AWS Actions that permit escalation of privileges.",
        default=None
    )
    ResourceExposure: List[str] = Field(
        title="Resource Exposure Findings",
        description="The IAM Policy allows actions that permit modification of resource-based policies or can "
                    "otherwise can expose AWS resources to the public",
        default=None
    )
    DataExfiltration: List[str] = Field(
        title="Data Exfiltration Findings",
        description="Data Exfiltration actions allow certain read-only IAM actions without resource constraints, such "
                    "as s3:GetObject, ssm:GetParameter*, or secretsmanager:GetSecretValue.",
        default=None
    )
    CredentialsExposure: List[str] = Field(
        title="Credentials Exposure Findings",
        description="Credentials Exposure actions return credentials as part of the API response , such as "
                    "ecr:GetAuthorizationToken, iam:UpdateAccessKey, and others",
        default=None
    )
    InfrastructureModification: List[str] = Field(
        title="Infrastructure Modification Findings",
        description="Infrastructure Modification describes IAM actions with 'modify' capabilities, and can therefore "
                    "lead to Resource Hijacking, unauthorized creation of Infrastructure, Backdoor creation, and/or"
                    " modification of existing resources which can result in downtime.",
        default=None
    )


@router.post("/scan-iam-policy", response_model=ScanPolicyResponse)
async def scan_iam_policy(
    item: ScanPolicyInput
):
    if item.include_actions is None:
        include_actions = INCLUDE_ACTIONS_DEFAULT
    else:
        include_actions = item.include_actions

    if item.exclude_actions is None:
        exclude_actions = EXCLUDE_ACTIONS_DEFAULT
    else:
        exclude_actions = item.exclude_actions

    exclusions_cfg = {
        "exclude-actions": exclude_actions,
        "include-actions": include_actions
    }
    body = scan_policy(item.policy_document, exclusions_cfg)
    return body
