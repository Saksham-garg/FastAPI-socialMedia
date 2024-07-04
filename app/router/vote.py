from fastapi import Depends,APIRouter,status,HTTPException
from .. import oauth2,database,schemas, models
from sqlalchemy.orm import Session

voteRouter = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@voteRouter.post('/',status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,db: Session = Depends(database.get_db),current_user: str = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Cannot like the post as post with {vote.post_id} doesn't found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    if (vote.dir == 1):
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Post with {vote.post_id} already found in vote")
        
        add_vote = models.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(add_vote)
        db.commit()
        return {"message":"Vote added successfully."}
    else:
        if not vote_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {vote.post_id} doesnot found in Vote")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return { "message":"Vote removed successfully."}

    



