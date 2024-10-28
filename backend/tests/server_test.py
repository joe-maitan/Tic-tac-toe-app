import pytest
import pymongo
from pymongo import MongoClient

from flask import Flask, json, request
from flask_cors import CORS

from flask_login import LoginManager
# from ..config import app  # import app from config because that is where the app is created


# Declare a mock fixture for the MongoDB client (this will be torn down after the tests)
@pytest.fixture
def mock_mongo(mocker):
    # Mock the MongoClient class
    mock_client = mocker.patch('pymongo.MongoClient')
    mock_database = mock_client.return_value
    mock_collection = mock_database.return_value
    mock_collection.insert_one.return_value = True

    return mock_client

@pytest.fixture()
def app():
    app = Flask(__name__)
    login_manager = LoginManager()
    login_manager.init_app(app)
    return app


@pytest.fixture()
def client(app):
    app.testing = True
    return app.test_client()


def test_signup_success(client, mock_mongo):
    data = {
        "username": "jjmaitan",
        "email": "jjm@gmail.com",
        "password": "1234567890"
    }

    response = client.post("/signup", data=data)  # Send a POST request with valid data

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Data: {response.json}") 

    assert response.status_code == 201   # Assert successful response code (201 Created)
    assert response.json == {"message": "User created successfully"}  # Assert expected success response message
    

def test_signup_invalid_data(client, mock_mongo):
    # Invalid data (missing username)
    data = {
        "email": "jjm@gmail.com",
        "password": "1234567890"
    }

    # Send a POST request with invalid data
    response = client.post("/signup", data=data)

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Data: {response.json}") 

    assert response.status_code == 400  # Assert expected error response code (e.g., 400 Bad Request)
    assert response.json == {"error": "Missing username"}  # Assert expected error response message

    

    

