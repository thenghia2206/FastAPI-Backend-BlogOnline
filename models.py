from database import Base
from sqlalchemy import Column,Integer,String, ForeignKey,Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__= "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title=Column(Text, nullable=False) 
    content=Column(Text, nullable=False)
    createdOn=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    updateOn=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    thumnail=Column(Text)
    desciption=Column(Text,nullable=False)
    numlike=Column(Integer,server_default = "0",nullable=False)
    numcmt=Column(Integer, server_default = "0",nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False )
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False )
    owner = relationship("User")
    category = relationship("Category")


class User(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name=Column(String(255),nullable=False)
    username= Column(String(255),nullable=False,unique=True)
    email= Column(String(255),nullable=False,unique=True)
    password = Column(String(255),nullable=False)
    avatar=Column(Text)
    role= Column(Integer,server_default ="0",nullable=False)
    post_status=Column(Integer,server_default = "0",nullable=False)
    cmt_status=Column(Integer,server_default = "0",nullable=False)
    time_ban=Column(TIMESTAMP(timezone=True))

class Category(Base):
    __tablename__= "category"
    id  = Column(Integer, primary_key=True, nullable=False)
    name= Column(String(255),nullable=False)

class Comment(Base):
    __tablename__= "comment"
    id = Column(Integer, primary_key=True, nullable=False)
    content=Column(Text, nullable=False)
    createdOn=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    updateOn=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False )
    post_id= Column(Integer, ForeignKey("posts.id"), nullable=False )
    name= Column(String(255), nullable=False)


class LikedComment(Base):
    __tablename__= "likedcomment"
    id = Column(Integer, primary_key=True, nullable=False)
    comment_id=Column(Integer, ForeignKey("comment.id"), nullable=False )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False )


class LikedPost(Base):
    __tablename__= "likedpost"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False )
    post_id= Column(Integer, ForeignKey("posts.id"), nullable=False )

