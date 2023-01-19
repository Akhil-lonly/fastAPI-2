from typing import List
from fastapi import Depends, FastAPI, status, HTTPException, UploadFile, File
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import schemas, database
from hashing import Hash
import models

SessionLocal = database.SessionLocal
engine = database.engine

models.Base.metadata.create_all(engine)
pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')
app = FastAPI()
User = schemas.User


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get a user with requested email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# get a user with requested phone number
def get_user_by_phone(db: Session, phone_number):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

# user registration after checking email and phone number
@app.post('/user', status_code=status.HTTP_201_CREATED)
def create(request: User, db: Session = Depends(get_db)):
    user_mail = get_user_by_email(db, email=request.email)
    user_phone = get_user_by_phone(db, phone_number=request.phone_number)
    if user_mail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email already registered")
    elif user_phone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phone number already exists")
    else:
        new_user = models.User(full_name=request.full_name, email=request.email, phone_number=request.phone_number,
                               password=Hash.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return new_user

# profile picture upload
@app.post("/user/{id}/profile_picture")
def upload_profile_picture(id: int, profile_picture: UploadFile = File(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    if not user.profile:
        user.profile = models.Profile()
        user.profile.profile_picture = profile_picture.filename
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# show the list of users
@app.get('/user', response_model=List[schemas.ShowUser])
def show_all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

#show a particular user with an id
@app.get('/user/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with an id:{id} not found ')
    return user
