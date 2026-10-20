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