from app.database.database import get_db
from app.models.tickets_models import Tickets
from app.database.database import Session
from sqlalchemy import or_, func
from app.exceptions.exceptions import TicketNotFound, CommentNotFound
from datetime import datetime, timezone
from app.models.comments_models import Comments
from app.models.users_models import Users


def get_ticket_or_404(db: Session,ticket_id: int)-> Tickets:

    founded = db.query(Tickets).filter(Tickets.id == ticket_id).first()
    
    if founded is None:
        raise TicketNotFound
    
    return founded

    
def list_tickets(db: Session,user: Users,title: str | None = None, offset: int = 0, limit: int = 20) -> list[Tickets]:

    query = db.query(Tickets).filter(Tickets.deleted.is_(False))

    if user.role != "admin":
        query = db.query(Tickets).filter(Tickets.user_id == user.id)

    if title:
        query = db.query(Tickets).filter(Tickets.title.ilike(f"%{title}%"))

    return query.order_by(Tickets.id).offset(offset).limit(limit).all()


def today_datetime():
    return datetime.now(timezone.utc).replace(microsecond=0)

def deleted_ticket(ticket):
    if ticket.deleted == True:
        return True
    return False



def search_comment(db: Session,comment_id:int) -> Comments:
    founded = db.query(Comments).filter(Comments.id == comment_id).first()

    if founded is None:
        raise CommentNotFound
        
    return founded