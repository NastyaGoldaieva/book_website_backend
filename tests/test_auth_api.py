import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

REGISTER_URL = "/api/register/"
LOGIN_URL = "/api/login/"
PROFILE_URL = "/api/profile/"

@pytest.mark.django_db
def test_register_success(api_client):
    payload = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "StrongPassword1"
    }
    res = api_client.post(REGISTER_URL, payload, format="json")
    assert res.status_code == status.HTTP_201_CREATED
    data = res.json()
    assert "access" in data and "refresh" in data and "user" in data
    assert data["user"]["username"] == "newuser"

@pytest.mark.django_db
def test_login_and_profile(api_client):
    user = User.objects.create_user(username="loginuser", email="login@example.com", password="Password123")
    res = api_client.post(LOGIN_URL, {"username": "loginuser", "password": "Password123"}, format="json")
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "access" in data and "refresh" in data
    token = data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    res2 = api_client.get(PROFILE_URL)
    assert res2.status_code == status.HTTP_200_OK
    assert res2.json().get("username") == user.username

@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    res = api_client.post(LOGIN_URL, {"username": "noone", "password": "bad"}, format="json")
    assert res.status_code == status.HTTP_400_BAD_REQUEST