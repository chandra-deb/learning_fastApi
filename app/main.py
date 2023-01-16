import os
import time
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("host")
db_name = os.getenv("dbname")
db_user = os.getenv("user")
db_password = os.getenv("password")


while True:
    try:
        conn = psycopg.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password,
            row_factory=dict_row,
        )
        cursor = conn.cursor()
        print("Successfully connect")
        break
    except Exception as error:
        print("Connecting to database failed")
        print(error)
        time.sleep(3)


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
def root(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"name": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"posts": posts}


@app.get("/posts/{id:int}")
def get_post(id: int, db: Session = Depends(get_db)):
    post: models.Post = db.query(models.Post).get(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found!",
        )

    return {"post": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """
        INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *
    """,
        (
            post.title,
            post.content,
            post.published,
        ),
    )
    new_post = cursor.fetchone()
    conn.commit()

    return {"post": new_post}


@app.delete("/posts/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """
        DELETE FROM posts WHERE id=%s RETURNING *
    """,
        (id,),
    )
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        conn.cancel()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found!",
        )
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id:int}")
def update_post(id: int, post: Post):
    # index = find_post_index(id)
    cursor.execute(
        """
        UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *
    """,
        (post.title, post.content, post.published, id),
    )

    updated_post = cursor.fetchone()

    if updated_post == None:
        conn.cancel()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found!",
        )
    conn.commit()

    return {"post": updated_post}
