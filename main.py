from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import auth, user

app = FastAPI(title="Auth API")

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=auth.router)
app.include_router(router=user.router)
