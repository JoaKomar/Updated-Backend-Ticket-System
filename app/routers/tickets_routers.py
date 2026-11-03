from fastapi import APIRouter, HTTPException, Depends
from app.auth.jwt import get_current_user
from app.database.database import get_db, Session
from app.models.users_models import Users
from app.models.tickets_models import Tickets
from app.schemas.tickets_schemas import TicketUser
from app.schemas.users_schemas import Profile
from sqlalchemy import func, or_
from app.exceptions.exceptions import TicketNotFound

router = APIRouter(prefix="/tickets")



@router.get("/me", response_model=Profile)
async def user_profile(user: Users = Depends(get_current_user)):

    return user
    

@router.post("/create")
async def create_ticket(ticket: TicketUser,
 user: Users = Depends(get_current_user),
 db: Session = Depends(get_db)):

    new_ticket = Tickets(title=ticket.title,
                         description=ticket.description,
                         status=ticket.status,
                         user_id=user.id)

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {"ID" : new_ticket.id,
    "created_ticket" : new_ticket.title,
            "from" : user.name,
            "date" : new_ticket.date}

@router.get("/{ticket_id}")
async def view_ticket(ticket_id:int,
                      title: str | None = None, 
                       user: Users = Depends(get_current_user),
                       db: Session = Depends(get_db)):

    search_ticket = db.query(Tickets).filter(or_(Tickets.id == ticket_id,
                                           func.lower(title) == func.lower(Tickets.title))).first()


    if search_ticket is None:
        raise TicketNotFound

    if user.role != "admin" and user.id != search_ticket.user_id:
        raise TicketNotFound

    return search_ticket
