import pytest
from pymongo import MongoClient
from pytest_mock_resources import create_mongo_fixture

from flask import Flask
from config import app, db
from server import *


@pytest.fixture()
def client():
    app.testing = True
    return app.test_client()


@pytest.fixture(autouse=True)
def mock_db(mocker):
    mock_db = mocker.patch('config.db')
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
    if db['users'].find_one({"username": "bobbybiceps"}):
        db['users'].delete_one({"username": "bobbybiceps"})

    test_user_information = {
        "username": "bobbybiceps",
        "email": "logic@gmail.com",
        "password": "Ultra85"
    }

    response = client.post('/signup', json=test_user_information)
    print(f"response: {response}")
    assert response.status_code == 201
    assert response.json == {"message": "User created successfully"}

    db['users'].delete_one({"username": "bobbybiceps"})
    

def test_signup_missing_data(client, mock_db):
    test_user_information = {
        "email": "jjm@gmail.com",
        "password": "123456"
    }

    response = client.post('/signup', json=test_user_information)
    print(f"{response}")
    assert response.status_code == 400
    assert response.json == {"error": "Missing username"}


def test_signup_existing_username(client, mock_db):
    test_user_information = {
        "username": "jjmaitan",
        "email": "jjm@gmail.com",
        "password": "123456"
    }

    response = client.post('/signup', json=test_user_information)
    assert response.status_code == 400
    assert response.json == {"error": "Username already exists. Please choose another."}


def test_signup_existing_email(client, mock_db):
    test_user_information = {
        "username": "temp_name",
        "email": "jjm@gmail.com",
        "password": "123456"
    }

    response = client.post('/signup', json=test_user_information)
    assert response.status_code == 400
    assert response.json == {"error": "Email already exists. Please choose another."}


def test_login(client):
    test_login_information = {
        "username": "jjmaitan",
        "password": "joePassword"
    }

    response = client.post('/login', json=test_login_information)
    assert response.status_code == 201
    assert response.json == {"message": "User logged in successfully"}


def test_login_missing_data_password(client):
    test_login_information = {
        "username": "jjmaitan"
    }

    response = client.post('/login', json=test_login_information)
    assert response.status_code == 400
    assert response.json == {"error": "Missing password"}


def test_login_missing_data_username(client):
    test_login_information = {
        "password": "joePassword"
    }

    response = client.post('/login', json=test_login_information)
    assert response.status_code == 400
    assert response.json == {"error": "Missing username"}


def test_login_invalid_username(client):
    test_login_information = {
        "username": "jjmaitan123",
        "password": "joePassword"
    }

    response = client.post('/login', json=test_login_information)
    assert response.status_code == 404
    assert response.json == {"error": "Username not found"}


def test_login_invalid_password(client):
    test_login_information = {
        "username": "jjmaitan",
        "password": "wrongPassword"
    }

    response = client.post('/login', json=test_login_information)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid password"}


def test_profile(client):
    test_login_information = {
        "username": "jjmaitan",
        "password": "joePassword"
    }
    client.post('/login', json=test_login_information)
    response = client.get('/profile')

    print(response)

    assert response.status_code == 200
    assert response.json == {"user_id": "jjmaitan", "is_authenticated": True}