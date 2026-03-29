from sqlalchemy.orm import Session
from . import models, schemas
from .utils.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_job_applications(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.JobApplication).filter(models.JobApplication.user_id == user_id).order_by(models.JobApplication.date_applied.desc()).offset(skip).limit(limit).all()

def create_job_application(db: Session, application: schemas.JobApplicationCreate, user_id: int):
    # Depending on pydantic version, model_dump() is preferred over dict()
    try:
        app_data = application.model_dump()
    except AttributeError:
        app_data = application.dict()
        
    db_app = models.JobApplication(**app_data, user_id=user_id)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def get_job_application(db: Session, application_id: int, user_id: int):
    return db.query(models.JobApplication).filter(models.JobApplication.id == application_id, models.JobApplication.user_id == user_id).first()

def update_job_application(db: Session, application_id: int, user_id: int, app_update: schemas.JobApplicationUpdate):
    db_app = get_job_application(db, application_id, user_id)
    if db_app:
        try:
            update_data = app_update.model_dump(exclude_unset=True)
        except AttributeError:
            update_data = app_update.dict(exclude_unset=True)
            
        for key, value in update_data.items():
            setattr(db_app, key, value)
        db.commit()
        db.refresh(db_app)
    return db_app

def delete_job_application(db: Session, application_id: int, user_id: int):
    db_app = get_job_application(db, application_id, user_id)
    if db_app:
        db.delete(db_app)
        db.commit()
        return True
    return False
