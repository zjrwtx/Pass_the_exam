from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
class User(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UsernameCheck(BaseModel):
    username: str
    
# 定义反馈创建模型
class FeedbackCreate(BaseModel):
    name: str
    email: EmailStr
    feedback: str

# 定义反馈读取模型
class FeedbackRead(FeedbackCreate):
    created_at: datetime