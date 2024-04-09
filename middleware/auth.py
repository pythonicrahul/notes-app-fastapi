from fastapi import Request, HTTPException, status
from common.utils import verify_token
import jwt

async def authentication(request: Request):
    print("Printing...")
    authorization_header = request.headers.get("Authorization")
    if authorization_header is None or not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing or invalid")
    
    token = authorization_header.replace("Bearer ", "")
    print(token)

    try:
        payload = await verify_token(token)
        print(payload)
        return payload.get("sub")
    except jwt.JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))


async def get_user_id(request: Request):
    print("Printing...")
    authorization_header = request.headers.get("Authorization")
    if authorization_header is None or not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing or invalid")

    token = authorization_header.replace("Bearer ", "")
    
    try:
        payload = await jwt.decode(token)
        return payload.get("user_id")
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")