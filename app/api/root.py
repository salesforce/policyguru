# pylint: disable=missing-module-docstring
from fastapi import APIRouter
from starlette.requests import Request
import logging

router = APIRouter()

logger = logging.getLogger()


@router.get("/")
async def read_main(request: Request):
    # some async operation could happen here
    print("ROOT DUDE")
    logger.debug("ROOT DUDE")
    if request.scope.get("aws.event"):
        data = {
            "msg": "I see you are running in AWS",
            "aws_event": request.scope["aws.event"],
            "url": request.url,
            "base_url": request.base_url,
            "headers": request.headers.raw
        }
    else:
        data = {
            "msg": "Hello World",
            "url": request.url,
            "base_url": request.base_url,
            "headers": request.headers.raw
        }
    print(data)
    return {"msg": "Hello World"}
