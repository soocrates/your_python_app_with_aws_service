from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import schemas, crud, database, models
from routers.auth import get_current_user
from utils.s3 import create_presigned_upload_url, create_presigned_download_url
import uuid

router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("/", response_model=List[schemas.JobApplicationResponse])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    applications = crud.get_job_applications(db, user_id=current_user.id, skip=skip, limit=limit)
    return applications

@router.post("/", response_model=schemas.JobApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application: schemas.JobApplicationCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_job_application(db=db, application=application, user_id=current_user.id)

@router.get("/{app_id}", response_model=schemas.JobApplicationResponse)
def read_application(app_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_app = crud.get_job_application(db, application_id=app_id, user_id=current_user.id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_app

@router.patch("/{app_id}", response_model=schemas.JobApplicationResponse)
def update_application(app_id: int, application: schemas.JobApplicationUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_app = crud.update_job_application(db, application_id=app_id, user_id=current_user.id, app_update=application)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_app

@router.delete("/{app_id}")
def delete_application(app_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    success = crud.delete_job_application(db, application_id=app_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"message": "Application deleted successfully"}

@router.post("/{app_id}/cv/upload")
def upload_cv(
    app_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_app = crud.get_job_application(db, application_id=app_id, user_id=current_user.id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")

    ext = file.filename.split('.')[-1] if '.' in file.filename else 'bin'
    object_key = f"cvs/{current_user.id}/{app_id}/{uuid.uuid4()}.{ext}"

    from utils.s3 import upload_file_to_s3
    upload_file_to_s3(file, object_key)

    # FIX: use Pydantic model, not dict
    update_model = schemas.JobApplicationUpdate(cv_s3_key=object_key)

    crud.update_job_application(
        db,
        application_id=app_id,
        user_id=current_user.id,
        app_update=update_model
    )

    return {"object_key": object_key, "message": "CV uploaded successfully"}

@router.get("/{app_id}/cv/download-url")
def get_cv_download_url(app_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_app = crud.get_job_application(db, application_id=app_id, user_id=current_user.id)
    if db_app is None or not db_app.cv_s3_key:
        raise HTTPException(status_code=404, detail="CV not found for this application")
        
    url = create_presigned_download_url(db_app.cv_s3_key)
    if not url:
        raise HTTPException(status_code=500, detail="Could not generate presigned URL")
        
    return {"url": url}
