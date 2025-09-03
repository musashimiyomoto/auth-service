from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from api.routers import auth, permission, user
from exceptions import BaseError
from usecases import PermissionUsecase


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Initializing permissions:")
    for perm in await PermissionUsecase().init_permissions():
        logger.info(f"{perm.role}: {perm.action} -> {perm.resource}")

    yield


app = FastAPI(title="Auth API", lifespan=lifespan)

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(exc_class_or_status_code=BaseError)
async def error_handler(request: Request, exc: BaseError) -> JSONResponse:
    """Error handler.

    Args:
        request: The request.
        exc: The exception.

    Returns:
        The JSON response.

    """
    return JSONResponse(content={"detail": exc.message}, status_code=exc.status_code)


app.include_router(router=auth.router)
app.include_router(router=user.router)
app.include_router(router=permission.router)
