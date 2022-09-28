import http
from fastapi import status, Depends, APIRouter, Response, HTTPException
import models
import schemas
from database import get_db
from sqlalchemy.orm import Session
from typing import List
import oauth2
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), curren_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).all()

    return post


@router.get("/user", response_model=List[schemas.Post])
def get_posts_user(db: Session = Depends(get_db), curren_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(
        models.Post.owner_id == curren_user.id).all()

    return post


@router.post("/add_post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def add_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.post_status == 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="ban post")

    posts = models.Post(owner_id=current_user.id, **post.dict())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts


@router.get("/{id}", response_model=schemas.Post)
def get_post_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return post


@router.delete("/delete_post/{id}")
def delete_post_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    post_delete = post.first()
    if post_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/update_post/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post_id(id: int, request: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if current_user.post_status == 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User banned post")

    post_old = db.query(models.Post).filter(models.Post.id == id,models.Post.owner_id == current_user.id )
    if not post_old.first():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Don't delete Post")
    post_old.update(request.dict(),synchronize_session= False)
    db.commit()
    return http.HTTPStatus.OK
