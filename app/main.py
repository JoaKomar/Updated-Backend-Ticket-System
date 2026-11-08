from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database.database import engine,Base
from app.routers.auth_routers import router as auth_router
from app.routers.tickets_routers import router as tickets_router
from app.routers.comments_routers import router as comments_router
from app.models.tickets_models import Tickets
from app.models.users_models import Users
from app.models.comments_models import Comments
from app.exceptions.exceptions import TicketNotFound, CommentNotFound

app = FastAPI()

app.include_router(auth_router)
app.include_router(tickets_router)
app.include_router(comments_router)

Base.metadata.create_all(engine)

@app.exception_handler(TicketNotFound)
async def manage_ticket_not_found(_request: Request, _exc:TicketNotFound):
    return JSONResponse(status_code=404,
                        content={"detail" : "Ticket Not Found"})


@app.exception_handler(CommentNotFound)
async def manage_comment_not_found(_request: Request, _exc:CommentNotFound):
    return JSONResponse(status_code=404,
                        content={"detail" : "Comment Not Found"})