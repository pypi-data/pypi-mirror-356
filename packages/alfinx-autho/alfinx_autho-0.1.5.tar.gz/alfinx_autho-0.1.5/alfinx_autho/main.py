import os
from fastapi import HTTPException, Request
import httpx

X_SERVICE_ORIGIN_CODE = os.getenv("X_SERVICE_ORIGIN_CODE")
AUTHENTICATION_API_URL = os.getenv("AUTHENTICATION_API_URL", "http://example.com/auth")

if not AUTHENTICATION_API_URL:
    raise RuntimeError("AUTHENTICATION_API_URL env var not set")
if not X_SERVICE_ORIGIN_CODE:
    raise RuntimeError("X_SERVICE_ORIGIN_CODE env var not set")

async def check_authentication(request: Request):
    headers = dict(request.headers)
    if "x-api-key" not in headers:
        raise HTTPException(
            status_code=401,
            detail=[{
                "type": "header",
                "loc": ["headers", "x-api-key"],
                "msg": "API key is missing.",
                "input": None,
            }],
        )
    if "x-service-code" not in headers:
        raise HTTPException(
            status_code=401,
            detail=[{
                "type": "header",
                "loc": ["headers", "x-service-code"],
                "msg": "Service code is missing.",
                "input": None,
            }],
        )
    auth_headers = {
        "x-api-key": headers["x-api-key"],
        "x-service-code": headers["x-service-code"],
        "x-service-origin-code": X_SERVICE_ORIGIN_CODE,
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(AUTHENTICATION_API_URL, headers=auth_headers)
    except httpx.RequestError as exc:
        raise HTTPException(
            detail=[{
                "type": "service",
                "loc": [],
                "msg": "Authentication service is unavailable.",
                "input": None,
            }],
        ) from exc

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=[{
                "type": "service",
                "loc": [],
                "msg": "Authentication failed.",
                "input": None,
            }],
        )
    masked_x_api_key = f"{auth_headers['x-api-key'][:6]}{auth_headers['x-api-key'][-6:]}"
    return masked_x_api_key, auth_headers["x-service-code"]
