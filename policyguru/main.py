# pylint: disable=missing-module-docstring
import os
from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
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

# Per https://github.com/chgangaraju/fastapi-mangum-example/blob/master/app/main.py
# https://github.com/jordaneremieff/mangum/issues/39#issuecomment-757535824
app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=[
        "x-apigateway-header", "Content-Type", "X-Amz-Date",
    ],
)

app.include_router(root.router)
app.include_router(scan_iam_policy.router)
app.include_router(write_iam_policy.router)

handler = Mangum(app, lifespan="off")
