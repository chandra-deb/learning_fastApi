import time
from fastapi import FastAPI, Response, status, HTTPException, Depends


import psycopg2
from psycopg2.extras import RealDictCursor
from .envar import *
from .database import engine, get_db
from sqlalchemy.orm import Session, Query
from . import models, schemas, utils

while True:
    try:
        conn = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Successfully connect")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(error)
        time.sleep(3)


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@app.get("/posts", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts: list[models.Post] = db.query(models.Post).all()

    return posts


@app.get("/posts/{id:int}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post: models.Post = db.query(models.Post).get(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found!",
        )

    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.delete("/posts/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post_query: Query = db.query(models.Post).where(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found!",
        )
    post_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id:int}", response_model=schemas.Post)
def update_post(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):

    post_query: Query = db.query(models.Post).where(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found!",
        )
    post_query.update(updated_post.dict())
    db.commit()
    db.refresh(post)

    return post


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users/{id:int}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user: models.User = db.query(models.User).get(id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found!",
        )
    return user
