"""
This module contains the status router for the API.
It provides endpoints for checking the status of the API and get the server's time.
SHOULD ALLOW ACCESS TO THIS ROUTER WITHOUT AUTH.
To enable metrics, pass enable_metrics=True and the auth_handler to the router.
>>> status_router.enable_metrics = True
>>> status_router.auth_handler = auth_handler
Then include the router in the FastAPI app.
>>> app.include_router(status_router)
"""

from datetime import datetime
from fastapi import APIRouter, Request
from typing import Annotated, Literal
from fastapi import APIRouter, Response, Depends
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from crypticorn.common.metrics import registry
from crypticorn.common.auth import AuthHandler

class EnhancedApiRouter(APIRouter):
    def __init__(self, enable_metrics: bool = False, auth_handler: AuthHandler = AuthHandler(), *args, **kwargs):
        """
        Enhanced API Router that allows for metrics and authentication.
        If enable_metrics is True, the router will include the metrics endpoint.
        If auth_handler is provided, the router will use the auth handler to authenticate requests with
        """
        super().__init__(*args, **kwargs)
        self.enable_metrics = enable_metrics
        self.auth_handler = auth_handler

router = EnhancedApiRouter(tags=["Status"], prefix="")


@router.get("/", operation_id="ping")
async def ping(request: Request) -> str:
    """
    Returns 'OK' if the API is running.
    """
    return "OK"


@router.get("/time", operation_id="getTime")
async def time(type: Literal["iso", "unix"] = "iso") -> str:
    """
    Returns the current time in either ISO or Unix timestamp (seconds) format.
    """
    if type == "iso":
        return datetime.now().isoformat()
    elif type == "unix":
        return str(int(datetime.now().timestamp()))


@router.get("/metrics", operation_id="getMetrics", include_in_schema=router.enable_metrics)
def metrics(username: Annotated[str, Depends(router.auth_handler.basic_auth)]):
    """
    Get Prometheus metrics for the application. Returns plain text.
    """
    return Response(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

