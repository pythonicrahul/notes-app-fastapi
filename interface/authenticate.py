from pydantic import BaseModel

class RegisterInterface(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class LoginInterface(BaseModel):
    email: str
    password: str
