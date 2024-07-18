from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# tipos de datos text, para textos largos
from typing import Text, Optional
from datetime import date, datetime
from uuid import uuid4 as uuid


app = FastAPI()

posts = []

# post model
class Post(BaseModel):
  # especifica los tipos de cada variable
  id: Optional[str]
  title: str 
  author: str 
  content: Text
  created_at: datetime= datetime.now()
  published_at: Optional[datetime]
  public: bool = False


@app.get('/')
def read_root():
  return {"welcome":"Welcome to my first API"}

@app.get('/posts')
def get_posts():
  return posts

@app.post('/posts')
# aqui se usan tipos de datos. Se espera que el dato sea de tipo Post
def save_posts(post: Post):
  post.id = str(uuid())
  print(uuid())
  posts.append(post.model_dump())
  return posts[-1]

@app.get('/posts/{post_id}')
def get_post(post_id: str):
  for post in posts:
    if post['id'] == post_id:
      return post
  return HTTPException(status_code=404, detail="Post Not Found")

@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
  index = 0
  for index,post in enumerate(posts):
    if post['id'] == post_id:
      posts.pop(index)
      return {"message": f"Post has {post_id} been deleted"}
  return HTTPException(status_code=404, detail="Post Not Found")

@app.put('/posts/{post_id}')
def update_post(post_id: str, updated_post: Post):
  for index, post in enumerate(posts):
    if post['id'] == post_id:
      posts[index]['title'] = updated_post.title
      posts[index]['content'] = updated_post.content
      posts[index]['author'] = updated_post.author
      return {"message":"Post updated successfully"}
  return HTTPException(status_code=404, detail="Post Not Found")