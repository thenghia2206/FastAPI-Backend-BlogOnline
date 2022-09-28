import http
from fastapi import status, Depends, APIRouter
import models
from database import get_db
from sqlalchemy.orm import Session
from typing import List
import oauth2
router = APIRouter(
    prefix="/like_post",
    tags=['Like']
)


@router.post("/{id}", status_code=status.HTTP_201_CREATED)
def like_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    like_post = db.query(models.LikedPost).filter(
        models.LikedPost.user_id == current_user.id, models.LikedPost.post_id == id)
    if like_post.count() != 0:
        like_post.delete(synchronize_session=False)
        db.commit()
        return http.HTTPStatus.OK
    liked_posts = models.LikedPost(user_id=current_user.id, post_id=id)
    db.add(liked_posts)
    db.commit()
    db.refresh(liked_posts)
    return http.HTTPStatus.OK


@router.get("/count_like/{id}")
def count_like_post(id: int, db: Session = Depends(get_db), curren_user: int = Depends(oauth2.get_current_user)):
    like = db.query(models.LikedPost).filter(
        models.LikedPost.post_id == id).count()
    return like

