from fastapi import Depends, APIRouter
import models
import schemas
from database import get_db
from sqlalchemy.orm import Session
from typing import List
import oauth2
router = APIRouter(
    prefix="/category",
    tags=['Category']
)

@router.get("/", response_model=List[schemas.Category])
def get_posts(db: Session = Depends(get_db), curren_user: int = Depends(oauth2.get_current_user)):
    category = db.query(models.Category).all()

    return category