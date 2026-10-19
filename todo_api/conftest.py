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
def temp_user(client):
    name = "t_" + secrets.token_hex(5)
    data = {'username':name,'password':"test12345"}
    r = client.post("/auth/register",json=data)
    assert r.status_code == 201,f"fixture 准备失败: {r.text}"
    yield data
    with db.engine.begin() as conn:
        conn.execute(text("""
                        DELETE FROM todos WHERE owner_id IN(
                        SELECT id FROM todo_users WHERE username = :u)
                        """),{"u":name})
        conn.execute(text("DELETE FROM todo_users WHERE username = :u"),{"u":name})
