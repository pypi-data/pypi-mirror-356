import pytest
from unittest.mock import patch, Mock
from netpy.http_client import HttpClient

@pytest.fixture
def client():
    return HttpClient(base_url="https://api.example.com")

def test_full_url_absolute(client):
    url = client._full_url("https://other.com/data")
    assert url == "https://other.com/data"

def test_full_url_relative(client):
    url = client._full_url("/endpoint")
    assert url == "https://api.example.com/endpoint"

def test_set_headers(client):
    headers = {"X-Test-Header": "value"}
    client.set_headers(headers)
    assert client.session.headers.get("X-Test-Header") == "value"

def test_set_user_agent(client):
    ua = "NetPyTest/1.0"
    client.set_user_agent(ua)
    assert client.session.headers.get("User-Agent") == ua

def test_set_cookies(client):
    cookies = {"sessionid": "abc123"}
    client.set_cookies(cookies)
    assert client.session.cookies.get("sessionid") == "abc123"

def test_set_auth(client):
    auth = ("user", "pass")
    client.set_auth(auth)
    assert client.session.auth == auth

def test_set_auth_bearer(client):
    token = "mytoken123"
    client.set_auth_bearer(token)
    assert client.session.headers.get("Authorization") == f"Bearer {token}"

@patch("netpy.http_client.requests.Session.get")
def test_get_request(mock_get, client):
    mock_response = Mock()
    mock_response.cookies = {"token": "123"}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    response = client.get("/test", params={"q": "value"})
    mock_get.assert_called_once()
    assert response == mock_response
    # The cookie from response should be stored in session.cookies
    assert client.session.cookies.get("token") == "123"

@patch("netpy.http_client.requests.Session.post")
def test_post_request(mock_post, client):
    mock_response = Mock()
    mock_response.cookies = {"token": "abc"}
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response

    response = client.post("/test", json={"key": "value"})
    mock_post.assert_called_once()
    assert response == mock_response
    assert client.session.cookies.get("token") == "abc"

@patch("netpy.http_client.requests.Session.put")
def test_put_request(mock_put, client):
    mock_response = Mock()
    mock_response.cookies = {"session": "xyz"}
    mock_response.raise_for_status = Mock()
    mock_put.return_value = mock_response

    response = client.put("/test", data={"key": "value"})
    mock_put.assert_called_once()
    assert response == mock_response
    assert client.session.cookies.get("session") == "xyz"

@patch("netpy.http_client.requests.Session.delete")
def test_delete_request(mock_delete, client):
    mock_response = Mock()
    mock_response.cookies = {"sid": "delete123"}
    mock_response.raise_for_status = Mock()
    mock_delete.return_value = mock_response

    response = client.delete("/test")
    mock_delete.assert_called_once()
    assert response == mock_response
    assert client.session.cookies.get("sid") == "delete123"
