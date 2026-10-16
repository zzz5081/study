FAKE_DB: dict[str,dict] = {}
_next_id = 0

def create_user(username: str,pwd_hash: bytes) -> int:
    global _next_id
    _next_id += 1
    FAKE_DB[username] = {
        'user_id':_next_id,
        'username': username,
        'pwd_hash': pwd_hash
    }
    return _next_id

def get_user(username: str) -> dict | None:
    user = FAKE_DB.get(username)
    if not user:
        return None
    return user