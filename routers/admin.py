import http
import models,schemas
from fastapi import  status, Depends,APIRouter,HTTPException
from database import  get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
import oauth2
router = APIRouter(
    prefix="/admin",
    tags=['Admin']
)

@router.get('/getAll_User',response_model= List[schemas.UserOut])
def get_All_User(db: Session = Depends(get_db) ,current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 0 :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"You are not Admin") 
    user = db.query(models.User).filter(models.User.role == 0).all()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Don't User")
    
    return user 

@router.delete("/delete_User/{id}")
def delete_User_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 0 :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"You are not Admin")
    user = db.query(models.User).filter(models.User.id == id, models.User.role == 0)
    users = user.first()
    if users == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User don't exist")

    user.delete(synchronize_session=False)
    db.commit()

    return http.HTTPStatus.OK

@router.put('/post_ban_User/{id}', status_code=status.HTTP_202_ACCEPTED)
def Ban_User_Post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 0 :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"You are not Admin")
    user = db.query(models.User).filter(models.User.id == id, models.User.role == 0)
    if user.filter(models.User.post_status == "1").first():
        user.update({"post_status":"0"},synchronize_session=False)
        db.commit()
        return http.HTTPStatus.OK
    if not user.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User don't exist")
    user.update({"post_status":"1"},synchronize_session=False)
    db.commit()
    return http.HTTPStatus.OK

@router.put('/comment_ban_User/{id}', status_code=status.HTTP_202_ACCEPTED)
def Ban_User_Comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 0:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"You are not Admin")
    user = db.query(models.User).filter(models.User.id == id, models.User.role == 0)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User don't exist")
    if user.filter(models.User.cmt_status == "1").first():
        user.update({"cmt_status":"0"},synchronize_session=False)
        db.commit()
        return http.HTTPStatus.OK
    user.update({"cmt_status":"1"},synchronize_session=False)
    db.commit()
    return http.HTTPStatus.OK

@router.put('/ban_User/{id}', status_code=status.HTTP_202_ACCEPTED)
def Ban_User(id: int,day: int , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 0:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"You are not Admin")
    user = db.query(models.User).filter(models.User.id == id, models.User.role == 0)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User don't exist")
    time_now = datetime.now()
    time_ban = datetime.now() + timedelta(days=day)
    if user.filter(models.User.time_ban > time_now).first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User banned")
    user.update({"time_ban": time_ban },synchronize_session=False)
    db.commit()
    return http.HTTPStatus.OK

@router.delete("/delete_post/{id}")
def delete_post_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 0:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"You are not Admin")
    post = db.query(models.Post).filter(models.Post.id == id)
    post.delete(synchronize_session=False)
    db.commit()

    return http.HTTPStatus.OK

@router.put('/unban_User/{id}', status_code=status.HTTP_202_ACCEPTED)
def Unban_User(id: int , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.role == 0:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"You are not Admin")
    user = db.query(models.User).filter(models.User.id == id, models.User.role == 0)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User don't exist")
    time_now = datetime.now()
    if user.filter(models.User.time_ban <= time_now).first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not banned")
    user.update({"time_ban": time_now },synchronize_session=False)
    db.commit()
    return http.HTTPStatus.OK