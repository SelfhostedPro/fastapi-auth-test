from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from db import models, crud, schemas, database
from sqlalchemy.orm import Session
from utils import get_db

router = APIRouter()

@router.post('/create', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already in use")
    return crud.create_user(db=db, user=user)


@router.post('/login')
def login(user: schemas.UserCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    _user = db.query(models.User).filter(models.User.username==user.username).first()
    if _user is not None and crud.verify_password(user.password, _user.hashed_password):
        return {'success': True}
    else:
        return {'failure': True}

    # access_token = Authorize.create_access_token(subject=user.username)
    # return {"access_token": access_token}