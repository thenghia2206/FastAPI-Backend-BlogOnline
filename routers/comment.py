import http
from fastapi import status, Depends, APIRouter, HTTPException
import models
import schemas
from database import get_db
from sqlalchemy.orm import Session
from typing import List
import oauth2
router = APIRouter(
    prefix="/comment",
    tags=['Comment']
)


@router.post("/create/{id}", response_model=schemas.Comment)
def create_comment(id: int, comments: schemas.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.cmt_status == 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="ban comment")
    comment = models.Comment(user_id=current_user.id,
                             post_id=id, name = current_user.name ,**comments.dict())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get('/{id}')
def get_comment(id: int, db: Session = Depends(get_db) ,curren_user: int = Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.post_id == id).all()
    return comment

@router.post("/like/{id}", status_code=status.HTTP_201_CREATED)
def like_comment_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    like_comment = db.query(models.LikedComment).filter(
        models.LikedComment.user_id == current_user.id, models.LikedComment.comment_id == id)
    if like_comment.count() != 0:
        like_comment.delete(synchronize_session=False)
        db.commit()
        return http.HTTPStatus.OK
    liked_comments = models.LikedComment(user_id=current_user.id,comment_id = id)
    db.add(liked_comments)
    db.commit()
    db.refresh(liked_comments)
    return http.HTTPStatus.OK

@router.get("/count_comment/{id}")
def count_like_comment(id: int, db: Session = Depends(get_db), curren_user: int = Depends(oauth2.get_current_user)):
    like = db.query(models.LikedComment).filter(
        models.LikedComment.comment_id == id).count()
    return like
