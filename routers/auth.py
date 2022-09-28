from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import database
import schemas
import models
import utils
import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

  user = db.query(models.User).filter(
      models.User.username == user_credentials.username).first()

  if not user:
        raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

  if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
  # Check Ban User
  if user.time_ban != None :
    time_now = datetime.now()
    if time_now < user.time_ban:
      raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN, detail=f"User Banned To {user.time_ban}")
  


  #create a token

  #return token
  access_token = oauth2.create_access_token(data={"user_id": user.id})

  return {"access_token": access_token , "token_type": "bearer"}
