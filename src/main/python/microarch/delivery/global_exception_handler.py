from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ErrorResponse:
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail


async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


async def handle_http_exception(request: Request, exc: StarletteHTTPException) -> JSONResponse:  # noqa: ARG001
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


def add_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(Exception)(handle_unexpected_exception)
    app.exception_handler(StarletteHTTPException)(handle_http_exception)
