from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str
    is_verified: bool = False

class UserInDB(User):
    hashed_password: str
