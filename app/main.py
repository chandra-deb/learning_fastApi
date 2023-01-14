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

