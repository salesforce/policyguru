# pylint: disable=missing-module-docstring
import os
from fastapi import FastAPI
from mangum import Mangum

from policyguru.version import VERSION
from policyguru.api import root, scan_iam_policy, write_iam_policy

TITLE = "PolicyGuru"
DESCRIPTION = "This is an API for Policy Sentry and Cloudsplaining."
DOCS_URL = "/docs"
REDOC_URL = "/redoc"
app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=VERSION,
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL,
)

app.include_router(root.router)
app.include_router(scan_iam_policy.router)
app.include_router(write_iam_policy.router)

handler = Mangum(app, enable_lifespan=False)
