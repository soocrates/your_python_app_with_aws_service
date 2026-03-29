from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from database import Base

class ApplicationStatus(str, enum.Enum):
    APPLIED = "Applied"
    INTERVIEWING = "Interviewing"
    REJECTED = "Rejected"
    OFFER = "Offer"
    WITHDRAWN = "Withdrawn"

class JobCategory(str, enum.Enum):
    CLOUD = "Cloud"
    DEVOPS = "DevOps"
    SOFTWARE_ENGINEERING = "Software Engineering"
    IT_SUPPORT = "IT Support"
    OTHER = "Other"

class UserRole(str, enum.Enum):
    USER = "User"
    ADMIN = "Admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    
    applications = relationship("JobApplication", back_populates="owner")

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    company = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(JobCategory), default=JobCategory.OTHER)
    date_applied = Column(DateTime(timezone=True), default=func.now())
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    cv_s3_key = Column(String(512), nullable=True)
    notes = Column(Text, nullable=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="applications")
