from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str = Field(example = "Phaneendhar")
    last_name: str = Field(example = "Ghajada")
    username: str = Field(example = "phani0416")
    password: str = Field(example = "password")
    contact_num: str = Field(example = "+91 81867392")


class User(BaseModel):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4) 
    first_name: str
    last_name: str
    username: str
    password: str
    contact_num: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_disabled: bool = False

class BadResponse(BaseModel):
    message: str = Field(example = "Bad Request")

class UserLogin(BaseModel):
    username : str = Field(example = "johndoe@gmail.com")
    password : str = Field(example = "password")

class UserLoginResponse(BaseModel):
    access_token : str = Field(example = "sjdbajdasbddfjasbfjshbafhbsjfhabsjfhabsjhbasbhcxn_xzxnznNkKdasddadsa")

class UserUpdate(BaseModel):
    first_name: str = Field(example = "Phaneendhar")
    last_name: str = Field(example = "Ghajada")
    contact_num: str = Field(example = "+91 81867392")

class UserPassword(BaseModel):
    password : str = Field(example = "new_password")

class UserPasswordResponse(BaseModel):
    message : str = Field(example = "successfully updated password")
