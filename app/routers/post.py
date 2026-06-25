from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from typing import Optional
from .. import models, schemas
from . import oauth2
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/posts", # all the routes in this router will have the prefix "/posts"
    tags=["posts"]
)

# @router.get("/", response_model=list[schemas.Post]) # response_model is used to specify the type of the response, it will automatically convert the response to the specified type.

@router.get("/", response_model=list[schemas.voteModel])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit: int = 10,skip: int = 0,search: Optional[str] = ""):
  
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # will show all the post created by the logged user
    try:
        posts = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True
        )
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    )   
        
        return posts
    
    except Exception as e:
        print("ERROR",repr(e))
        raise

# the order of the routes whoever is defined first will be executed first. 
# so if we define the root route ("/") after the get_posts route, 
# it will never be executed because the root route will match all the requests. 
# so we should define the root route at the end of the file.

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # status code for created resource is 201
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() # commit the changes to the database
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post) # add the new post to the database session
    db.commit() # commit the changes to the database
    db.refresh(new_post) # refresh the new post to get the id from the database
    return new_post

# with Schema Validation, we can ensure that the data we receive in the request body is in the correct format.
# if we send a request with invalid data, we will get a 422 Unprocessable Entity

@router.get("/{id}" ,response_model=schemas.voteModel) # response_model is used to specify the type of the response, it will automatically convert the response to the specified type.
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    # 
    post = db.query(models.Post).filter(models.Post.id == id).first() # query the post with the given id from the database using SQLAlchemy ORM

    post = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True
        )
        .group_by(models.Post.id).filter(models.Post.id == id).first()
    )

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This action is forbidden")
    
    db.delete(post)
    db.commit()
    return {"message": f"Post with id: {id} was deleted successfully!"}
    

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    # conn.commit()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This action is forbidden")
    post_query.update(updated_post.dict(), synchronize_session=False) 
    db.commit()
    return post_query.first()
