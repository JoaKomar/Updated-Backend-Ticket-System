from app.database.database import get_db
from app.models.tickets_models import Tickets
from app.database.database import Session
from sqlalchemy import or_, func
from app.exceptions.exceptions import TicketNotFound, CommentNotFound
from datetime import datetime, timezone
from app.models.comments_models import Comments



def search_ticket(db,ticket_id:int, title: str | None = None) -> Tickets:
    founded = db.query(Tickets).filter(or_(Tickets.id == ticket_id,
                                           func.lower(title) == func.lower(Tickets.title))).first()
    
    if founded is None:
        raise TicketNotFound
    
    return founded


def check_properties(founded_ticket,user):
    if user.role != "admin" and user.id != founded_ticket.user_id:
        return False
    
    return True


def today_datetime():
    return datetime.now(timezone.utc).replace(microsecond=0)

def deleted_ticket(ticket):
    if ticket.deleted == True:
        return True
    return False



def search_comment(db,comment_id:int) -> Comments:
    founded = db.query(Comments).filter(Comments.id == comment_id).first()

    if founded is None:
        raise CommentNotFound
        
    return founded