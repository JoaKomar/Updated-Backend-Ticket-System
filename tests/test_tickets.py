import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_auth import db, user, user_auth_header, admin_auth_header,admin
from app.models.tickets_models import Tickets

client = TestClient(app)

@pytest.fixture
def create_ticket(user,db):

    new_ticket = Tickets(title="test",
                         description="testing for example",
                         status="pending",
                         user_id=user.id)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    try:
        yield new_ticket
    finally:
        db.delete(new_ticket)
        db.commit()


def test_view_tickets(user_auth_header):
    response = client.get("/tickets/me",
                          headers=user_auth_header)

    assert response.status_code == 200


def test_create_ticket(db,user,user_auth_header):
    response = client.post("/tickets/create",
                           headers=user_auth_header,
                           json={"title" : "test",
                                 "description" : "testing for example",
                                 "status" : "pending",
                                 "user_id" : user.id})

    assert response.status_code == 200

    response_id = response.json()["ID"]

    ticket_id = db.query(Tickets).filter(Tickets.id == response_id).first()

    db.delete(ticket_id)
    db.commit()



def test_view_ticket(user_auth_header,create_ticket):

    response = client.get(f"/tickets/{create_ticket.id}",
                          headers=user_auth_header)

    assert response.status_code == 200



def test_update_ticket(user_auth_header,create_ticket):

    response = client.put(f"/tickets/{create_ticket.id}",
                          headers=user_auth_header,
                          json={"title" : "updating",
                                "description" : "updating for example",
                                "status" : "pending"})

    assert response.status_code == 200




def test_delete_ticket(create_ticket,admin_auth_header):
    response = client.delete(f"/tickets/{create_ticket.id}",
                             headers=admin_auth_header)

    assert response.status_code == 200