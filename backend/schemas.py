from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from models import ApplicationStatus, JobCategory, UserRole

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: UserRole

    class Config:
        orm_mode = True
        from_attributes = True # pydantic v2

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class JobApplicationBase(BaseModel):
    title: str
    company: str
    description: Optional[str] = None
    category: JobCategory = JobCategory.OTHER
    status: ApplicationStatus = ApplicationStatus.APPLIED
    notes: Optional[str] = None

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplicationUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    category: Optional[JobCategory] = None
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None
    cv_s3_key: Optional[str] = None

class JobApplicationResponse(JobApplicationBase):
    id: int
    date_applied: datetime
    cv_s3_key: Optional[str] = None
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True
