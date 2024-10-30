import pytest
from flask import Flask

from config import app, db
from server import *


@pytest.fixture()
def client():
    app.testing = True
    return app.test_client()


@pytest.fixture(autouse=True)
def mock_db(mocker):
    mock_db = mocker.patch('db')
    mock_users_collection = mock_db.get_collection('users')

    # Setup mock responses for the collection
    mock_users_collection.find_one.return_value = None  # No user found
    mock_users_collection.insert_one.return_value = None  # Simulate successful insertion

    return mock_db


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!"}


def test_signup(client, mock_db):
    mock_db.get_collection('users').find_one.return_value = None
    test_user_information = {
        "username": "bobbybiceps",
        "email": "logic@gmail.com",
        "password": "Ultra85"
    }

    response = client.post('/signup', json=test_user_information)
    print(f"response: {response}")
    assert response.status_code == 201
    assert response.json == {"message": "User created successfully"}
    mock_db.get_collection('users').insert_one.assert_called_once()


def test_signup_missing_data(client, mock_db):
    test_user_information = {
        "email": "jjm@gmail.com",
        "password": "123456"
    }

    response = client.post('/signup', json=test_user_information)
    print(f"{response}")
    assert response.status_code == 400
    assert response.json == {"error": "Missing username"}


def test_signup_existing_email(client, mock_db):
    test_user_information = {
        "username": "jjmaitan",
        "email": "jjm@gmail.com",
        "password": "123456"
    }

    response = client.post('/signup', json=test_user_information)
    print(f"{response}")
    assert response.status_code == 400


def test_login(client):
    pass
