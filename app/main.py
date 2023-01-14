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

