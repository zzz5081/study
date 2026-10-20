import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
sys.path.insert(0, str(Path(__file__).parent))
from main import app
import secrets
import db
from sqlalchemy import text

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def temp_user(client,cleanup):
    name = "t_" + secrets.token_hex(5)
    cleanup.append(name)
    data = {'username':name,'password':"test12345"}
    r = client.post("/auth/register",json=data)
    assert r.status_code == 201,f"fixture 准备失败: {r.text}"
    return data

@pytest.fixture
def cleanup():
    names = []
    yield names
    with db.engine.begin() as conn:
        for n in names:
            conn.execute(
                text("DELETE FROM todos WHERE owner_id IN (SELECT id FROM todo_users WHERE username = :u)"),
                {"u": n},
            )
            conn.execute(text("DELETE FROM todo_users WHERE username = :u"),{"u": n})

@pytest.fixture
def auth_user(client,cleanup):
    name = "t_" + secrets.token_hex(5)
    cleanup.append(name)
    data = {"username": name,"password":"test12345"}
    client.post("/auth/register",json=data)
    r = client.post("/auth/login",json=data)
    token = r.json()["access_token"]
    return{
        "username": name,
        "headers": {"Authorization": f"Bearer {token}"}
    }

@pytest.fixture
def make_user(client,cleanup):
    def _make():
        name = "t_" + secrets.token_hex(5)
        cleanup.append(name)
        data = {"username": name ,"password": "test12345"}
        client.post("/auth/register",json=data)
        r = client.post("/auth/login",json=data)
        token = r.json()["access_token"]
        return {"username": name, "headers": {"Authorization": f"Bearer {token}"}}
    return _make