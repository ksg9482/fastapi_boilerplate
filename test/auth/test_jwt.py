import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.auth.jwt import get_user, create_access_token, authenticate_user

test_fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

@pytest.fixture
def user_service(user_repository):
    return get_user(user_repository, test_fake_users_db["johndoe"].get("username"))

@pytest
def test_create_access_token():
    access_token = create_access_token()
    assert access_token == True

@pytest
def test_authenticate_user(user_service):
    get_user = Mock().return_value = test_fake_users_db["johndoe"]
    result = authenticate_user(test_fake_users_db, test_fake_users_db["johndoe"].get("username"), test_fake_users_db["johndoe"].get("password"))
    assert result == test_fake_users_db