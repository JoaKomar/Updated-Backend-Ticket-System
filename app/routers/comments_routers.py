from fastapi import APIRouter, HTTPException, Depends
from app.auth.jwt import get_current_user, get_current_admin
from app.database.database import get_db, Session
from app.models.users_models import Users
from app.models.tickets_models import Tickets
from app.models.comments_models import Comments
from app.schemas.comments_schemas import CommentsUser
from app.schemas.tickets_schemas import TicketUser
from app.schemas.users_schemas import Profile
from app.exceptions.exceptions import CommentNotFound
from app.services.services import search_ticket,search_comment, check_properties, today_datetime, deleted_ticket


router = APIRouter(prefix="/comments")


@router.post("/create/{ticket_id}")
async def create_comments(ticket_id:int,
                        comment: CommentsUser,
                        user: Users = Depends(get_current_user), 
                        db: Session = Depends(get_db)):

    searched = search_ticket(db,ticket_id)

    if user.role != "admin":
        if searched.user_id != user.id:
            raise HTTPException(status_code=404, detail="Not Found")

    new_comment = Comments(content=comment.content,
                           user_id=user.id,
                           ticket_id=ticket_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {"details" : "your comment has been added"}

@router.get("/{comment_id}")
async def view_comments(comment_id:int,
                        user: Users = Depends(get_current_user),
                        db: Session = Depends(get_db)):

    searched = search_comment(db,comment_id)


    if user.role != "admin":

        if searched.deleted == True:
            raise HTTPException(status_code=404,detail="Not Found")
        
        if searched.ticket.user_id != user.id: 
            raise HTTPException(status_code=404, detail="Not Found")

    return {"id" : searched.id,
            "content" : searched.content,
            "date" : searched.date,
            "user_id" : searched.user_id,
            "ticket_id" : searched.ticket_id}


@router.put("/{comment_id}")
async def update_comment(comment_id: int,
                         new_comment: CommentsUser,
                         user: Users = Depends(get_current_user),
                         db: Session = Depends(get_db)):

    searched = search_comment(db,comment_id)

    if user.role != "admin":
        if searched.user_id != user.id:
            raise HTTPException(status_code=404,detail="Not Found")

    searched.content = new_comment.content

    db.commit()
    db.refresh(searched)

    return {"detail" : "your comment has been updated"}


@router.delete("/{comment_id}")
async def delete_comment(comment_id:int,
                         admin: Users = Depends(get_current_admin),
                         db: Session = Depends(get_db)):

    searched = search_comment(db,comment_id)

    searched.deleted = True

    db.commit()
    db.refresh(searched)

    return {"detail" : "the ticket has been successfully deleted"}
