from flask import json

from main import app


def test_get_blogs():
    response = app.test_client().get("/blogposts")
    blogs = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert type(blogs) is dict
    assert blogs["1"]["id"] == 1
    assert blogs["1"]["title"] == "Postman Title Update try one more time"
    assert len(blogs) == 5


def test_get_blog_by_id():
    response = app.test_client().get("/blogposts/2")
    post = json.loads(response.data.decode("utf-8"))
    print(type(post))
    assert response.status_code == 200
    assert type(post) is dict
    assert post["id"] == 2
    assert post["title"] == "Title 2"
    assert post["subtitle"] == ''
    assert post["body"] == "Body 2"


def test_update_blog():
    response = app.test_client().put("/blogposts/1", json={
        "id": "1",
        "title": "Title 1",
        "subtitle": "PUT test",
        "body": "Body 1."
    })
    post = json.loads(response.data)
    assert response.status_code == 200
    assert post["id"] == "1"


def test_create_blog():
    response = app.test_client().post("/blogposts", json={
        "id": "6",
        "title": "Title 6",
        "subtitle": "POST test",
        "body": "Body 6."
    })
    post = json.loads(response.data)
    assert response.status_code == 200
    assert post["title"] == "Title 6"


def test_delete_post():
    response = app.test_client().delete("/blogposts/6")
    post = json.loads(response.data)
    assert response.status_code == 200
    assert post["title"] == "Title 6"
    assert type(post['id']) is str
    assert isinstance(post['id'], str)
    assert not isinstance(post['id'], int)
    assert 'body' in post
