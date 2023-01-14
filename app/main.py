class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/posts")
def get_posts():
    cursor.execute(
        """
        SELECT * FROM posts
    """
    )
    posts = cursor.fetchall()

    return {"posts": posts}


@app.get("/posts/{id:int}")
def get_post(id: int):
    cursor.execute(
        """
        SELECT * FROM posts WHERE id=%s
    """,
        (id,),
    )
    post = cursor.fetchone()
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

