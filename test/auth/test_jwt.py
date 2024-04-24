import pytest
from src.auth.jwt import create_access_token


@pytest
def test_create_access_token():
    access_token = create_access_token()
    assert access_token == True
