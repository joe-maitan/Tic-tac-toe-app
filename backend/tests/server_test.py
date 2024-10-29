import pytest
from flask import Flask

from config import app, db
from server import *


@pytest.fixture()
def client():
    app.testing = True
    return app.test_client()

@pytest.fixture
def mock_mongo(mocker):
    # Mock the MongoClient class
    mock_client = mocker.patch('pymongo.MongoClient')
    mock_database = mock_client.return_value
    mock_collection = mock_database.return_value
    mock_collection.insert_one.return_value = True

    return mock_client


def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!"}


def test_signup(client):
    test_user_information = {
        "username": "jjmaitan",
        "email": "jjm@gmail.com",
        "password": "123456"
    }

    response = client.post('/signup', json=test_user_information)
    print(f"response: {response}")
    assert response.status_code == 201
    assert response.json == {"message": "User created successfully."}


def test_login(client):
    pass
