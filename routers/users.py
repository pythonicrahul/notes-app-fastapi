from interface.authenticate import LoginInterface, RegisterInterface
from common.utils import generate_token, epoch_time_after_minutes
import bcrypt
from bson import ObjectId
from interface.enums import USERS_COLLECTION
from connections.database import db
from fastapi import APIRouter, Header
from middleware.auth import get_user_id

user_router = APIRouter()

users_collection = db[USERS_COLLECTION]

@user_router.post("/register")
async def register(body: RegisterInterface):
    try:

        count = await users_collection.count_documents({"email": body.email})
        if count:
            return {
                "status": False,
                "message": "Email is already registered",
                "data": None
            }

        users = await users_collection.insert_one({
            "first_name": body.first_name,
            "last_name": body.last_name,
            "email": body.email,
            "password": bcrypt.hashpw(body.password, bcrypt.gensalt( 12 )),
        })

        token = await generate_token({ 
            "sub": str(users.inserted_id),
            "exp": epoch_time_after_minutes(60),
            "iat": epoch_time_after_minutes(),
            "name": body.first_name,
            "email": body.email
        })

        return {
            "data": {
                "token": token
            },
            "status": True,
            "message": "Successfully registered"
        }
    except Exception as e:
        print(e)
        return {    
            "data": None,
            "status": False,
            "message": str(e)
        }

@user_router.post("/login")
async def login(body: LoginInterface):
    try:
        user = await users_collection.find_one({"email": body.email})
        if user:
            if bcrypt.checkpw(body.password, user['password']):

                token = await generate_token({
                    "sub": str(user['_id']),
                    "exp": epoch_time_after_minutes(60),
                    "iat": epoch_time_after_minutes(),
                    "name": user['first_name'],
                    "email": user['email']
                })
                return {
                    "data": {
                        "token": token
                    },
                    "status": True,
                    "message": "Login successful"
                }
        return {
            "data": None,
            "status": False,
            "message": "Invalid email or password"
        }
    except Exception as e:
        print(e)
        return {    
            "data": None,
            "status": False,
            "message": str(e)
        }

@user_router.get("/user/{user_id}")
async def user_details(user_id: str, sub: str = Header(None, converter=get_user_id)):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    # print(sub)
    if user is not None:
        return {
            "data": {
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "email": user["email"]
            },
            "message": "User Found",
            "status": True
        }
    else:
        return {
            "status": False,
            "message": "User not found",
            "data": None
        }
    
