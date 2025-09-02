from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routers import auth, user
from exceptions import BaseError

app = FastAPI(title="Auth API")

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
