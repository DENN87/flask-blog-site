import pytest
from flask import g, session
from flaskr.db import get_db

# test sign up
def test_signup(client, app):
    assert client.get('/auth/signup').status_code == 200
    response = client.post(
        '/auth/signup', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/signin' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/signup',
        data={'username': username, 'password': password}
    )
    assert message in response.data


# test sign in
def test_signin(client, auth):
    assert client.get('/auth/signin').status_code == 200
    response = auth.signin()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.signin(username, password)
    assert message in response.data


# test logout
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session