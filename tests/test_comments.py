import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.test_auth import db, user

client = TestClient(app)


