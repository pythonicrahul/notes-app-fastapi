from fastapi import FastAPI, Depends, Request, HTTPException
from routers.users import user_router
from common.utils import verify_token

app = FastAPI()


# @app.middleware("http")


# app.include_router(user_router, prefix="/api/v1/", tags=["users"], dependencies=[Depends(authentication)])
app.include_router(user_router, prefix="/api/v1", tags=["users"])