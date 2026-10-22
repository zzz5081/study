def test_list_only_own(client,make_user):
    A = make_user()
    B = make_user()
    client.post("/todos",json={"title": "A 的待办"},headers=A["headers"])
    client.post("/todos",json={"title": "B 的待办"},headers=B["headers"])
    r = client.get("/todos",headers=A["headers"])

    assert r.status_code == 200
    titles = [t["title"] for t in r.json()]
    assert "A 的待办" in titles
    assert "B 的待办" not in titles

def test_create_todo(client,auth_user):
    r = client.post("/todos",json={"title":"买菜"},headers=auth_user["headers"])
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "买菜"
    assert body["done"] is False
    assert "id" in body

def test_patch_own(client,auth_user):
    h = auth_user["headers"]
    tid = client.post("/todos",json={"title": "原稿"},headers = h).json()["id"]     

    r = client.patch(f"/todos/{tid}",json={"done": True},headers = h)
    assert r.status_code == 200

    items = client.get("/todos",headers = h).json()
    that = [t for t in items if t["id"] == tid][0]
    assert that["done"] is True

def test_patch_partial(client,auth_user):
    h = auth_user["headers"]
    tid = client.post("/todos",json={"title": "原稿"},headers = h).json()["id"]

    client.patch(f"/todos/{tid}",json={"done": True},headers = h)

    r = client.patch(f"/todos/{tid}",json={"title": "新稿"},headers = h)
    assert r.json()["title"] == "新稿"
    assert r.json()['done'] is True

def test_delete_own(client,auth_user):
    h = auth_user["headers"]
    tid = client.post("/todos",json={"title": "去图书馆"},headers = h).json()["id"]

    client.delete(f"/todos/{tid}",headers = h)

    items = client.get("/todos",headers = h).json()
    assert not items

def test_patch_other_404(client,make_user):
    A = make_user()
    B = make_user()

    tid = client.post("/todos",json={"title": "健身"},headers=A["headers"]).json()['id']
    r = client.patch(f"/todos/{tid}",json={"title": "游泳"},headers=B['headers'])
    assert r.status_code == 404

def test_delete_other_404(client,make_user):
    A = make_user()
    B = make_user()

    tid = client.post("/todos",json = {'title': "有氧"},headers = A["headers"]).json()["id"]
    r = client.delete(f"/todos/{tid}",headers=B["headers"])
    assert r.status_code == 404

def test_todo_requires_token(client,auth_user):
    h = auth_user
    tid = client.post("/todos",json={"title": "健身"},headers=h['headers']).json()['id']
    r = client.patch(f"/todos/{tid}",json = {"done" : True})
    assert r.status_code == 401