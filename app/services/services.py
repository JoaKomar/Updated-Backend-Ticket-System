from app.database.database import get_db
from app.models.tickets_models import Tickets
from app.database.database import Session
from sqlalchemy import or_, func
from app.exceptions.exceptions import TicketNotFound
from datetime import datetime, timezone



def search_ticket(db,ticket_id:int, title: str | None = None) -> object | None:
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