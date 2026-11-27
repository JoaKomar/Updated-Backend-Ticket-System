import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_auth import db, user,user_auth_header,another_user,another_user_auth_header, admin_auth_header,admin
from app.models.comments_models import Comments
from tests.test_tickets import create_ticket
from app.models.users_models import Users
from app.auth.jwt import hash_password

client = TestClient(app)

@pytest.fixture
def create_comment(db,user,create_ticket):
    new_comment = Comments(content="i couldn't fix the bug",
                           user_id=user.id,
                           ticket_id=create_ticket.id)

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    try:
        yield new_comment
    finally:
        db.delete(new_comment)
        db.commit()

def test_create_comments(db,create_ticket,user_auth_header):
    
    response = client.post(f"/comments/create/{create_ticket.id}",
                               json={"content" : "i couldn't fix the bug"},
                                headers=user_auth_header)


    assert response.status_code == 200

    comment_id = response.json()["id"]

    query = db.query(Comments).filter(Comments.id == comment_id).first()

    db.delete(query)
    db.commit()

def test_view_comment(create_comment,user_auth_header):
    response = client.get(f"/comments/{create_comment.id}",
                          headers=user_auth_header)

    assert response.status_code == 200
    assert len(response.json()) > 0


def test_invalid_view_comment(user_auth_header):
    
    response = client.get(f"/comments/{-1}",
                          headers=user_auth_header)


    assert response.status_code == 404


def test_invalid_user_view_comment(create_comment,another_user_auth_header):
   

    response = client.get(f"/comments/{create_comment.id}",
                          headers=another_user_auth_header)

    assert response.status_code == 404

  

def test_update_comment(user_auth_header,create_comment):
    response = client.put(f"/comments/{create_comment.id}",
                          json={"content" : "updated comment for example"},
                          headers=user_auth_header)

    assert response.status_code == 200

def test_invalid_update_comment(create_comment,another_user_auth_header):
    response = client.put(f"/comments/{create_comment.id}",
                          json={"content" : "updated comment for example (invalid update)"},
                          headers=another_user_auth_header)

    assert response.status_code == 404

def test_delete_comment(admin_auth_header,create_comment):
    response = client.delete(f"/comments/{create_comment.id}",
                             headers=admin_auth_header)

    assert response.status_code == 200

def test_invalid_delete_comment(user_auth_header,create_comment):
    response = client.delete(f"/comments/{create_comment.id}",
                             headers=user_auth_header)

    assert response.status_code == 403