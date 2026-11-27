import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import SessionLocal
from app.auth.jwt import hash_password

from app.models.users_models import Users
import uuid


client = TestClient(app)


@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def user(db):
    hashed = hash_password("12345678")

    new_user = Users(name="test",
                     age=30,
                     email=f"test{str(uuid.uuid4())[:8]}@gmail.com",
                     password_hash=hashed)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        yield new_user

    finally:
        db.delete(new_user)
        db.commit()

@pytest.fixture
def another_user(db):
    hashed = hash_password("12345678")
    
    new_user = Users(name="test",
                         age=30,
                         email=f"test{str(uuid.uuid4())[:8]}@gmail.com",
                         password_hash=hashed)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        yield new_user

    finally:
        db.delete(new_user)
        db.commit()

@pytest.fixture
def another_user_auth_header(another_user):

    login = client.post("/auth/login",
                        json={"email" : another_user.email,
                              "password" : "12345678"})

    token = login.json()["access_token"]

    return {"Authorization" : f"Bearer {token}"}


    

@pytest.fixture
def admin(db):
    hashed = hash_password("12345678")

    new_user = Users(name="test",
                     age=30,
                     email=f"test{str(uuid.uuid4())[:8]}@gmail.com",
                     password_hash=hashed,
                     role="admin")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    try:
        yield new_user
    finally:
        db.delete(new_user)
        db.commit()



@pytest.fixture
def user_auth_header(user):
    response = client.post("/auth/login",
                           json={"email" : user.email,
                            "password" : "12345678"})
    

    token = response.json()["access_token"]

    return {"Authorization" : f"Bearer {token}"}


@pytest.fixture
def admin_auth_header(admin):
    response = client.post("/auth/login",
                           json={"email" : admin.email,
                           "password" : "12345678"})
    

    token = response.json()["access_token"]

    return {"Authorization" : f"Bearer {token}"}


def test_invalid_login(user):
    response = client.post("/auth/login",
                            json={"email" : user.email,
                            "password" : "12345678910"})

    assert response.status_code == 401


def test_invalid_register(user):
    response = client.post("/auth/register", json={"name" : "test",
                                                   "age" : 20,
                                                   "email" : user.email,
                                                   "password" : "12345678"})

    assert response.status_code == 409

    
def test_register_unprocessable_content():
    response = client.post("/auth/register", json={"name" : "aa",
                                                   "age" : 20,
                                                   "email" : "test@gmail.com",
                                                   "password" : "12345678"})

    assert response.status_code == 422


def test_login_unprocessable_content():
    response = client.post("/auth/login", json={"email" : "test@gmail.com",
                                                   "password" : "123456"})

    assert response.status_code == 422


def test_not_found_user():
    response = client.post("/auth/login", json={"email" : f"test{str(uuid.uuid4())[:8]}@gmail.com",
                                                "password" : "12345678"})

    assert response.status_code == 401


def test_invalid_password(user):
    response = client.post("/auth/login", json={"email" : user.email,
                                                "password" : "99999999999"})

    assert response.status_code == 401


def test_valid_token(user):
    response = client.post("/auth/login", json={"email" : user.email,
                                                "password" : "12345678"})
    assert response.json()["token_type"] == "Bearer"

    token = response.json()["access_token"]

    assert token is not None


def test_deleted_user(user,db):
    user.deleted = True

    db.commit()
    db.refresh(user)

    response = client.post("/auth/login", json={"email" : user.email,
                                                "password" : "12345678"})

    assert response.status_code == 401