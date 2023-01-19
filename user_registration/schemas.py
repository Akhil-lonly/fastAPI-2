from pydantic import BaseModel, EmailStr


class Profile(BaseModel):
    profile_picture: str

    class Config():
        orm_mode = True


class User(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: int
    password: str

# user details show model
class ShowUser(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: int

    class Config():
        orm_mode = True
