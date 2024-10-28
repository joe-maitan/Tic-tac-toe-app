import pytest
import pymongo

from flask import json, request
from pymongo import MongoClient
from config import app  # import app from config because that is where the app is created


# Declare a mock fixture for the MongoDB client (this will be torn down after the tests)
@pytest.fixture
def mock_mongo(mocker):
    # Mock the MongoClient class
    mock_client = mocker.patch('pymongo.MongoClient')
    mock_database = mock_client.return_value
    mock_collection = mock_database.return_value

    # Customize the mock behavior as needed (optional)
    # For example, simulate a successful user creation
    mock_collection.insert_one.return_value = True

    return mock_client


@pytest.fixture
def client():
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client


@pytest.mark.usefixtures("mock_mongo")
def test_signup_success(client):
    # Valid user data
    data = {
        "username": "jjmaitan",
        "email": "jjm@gmail.com",
        "password": "1234567890"
    }

    # Send a POST request with valid data
    response = client.post("/signup", data=data)

    print(f"Response data {response.data}")
    print(f"Response Status Code: {response.status_code}")  # Add print statement
    print(f"Response Data: {response.json}")  # Add print statement

    # Assert successful response code (201 Created)
    assert response.status_code == 201
    # Assert successful response message
    

@pytest.mark.usefixtures("mock_mongo")
def test_signup_invalid_data(client):
    # Invalid data (missing username)
    data = {
        "email": "jjm@gmail.com",
        "password": "1234567890"
    }

    # Send a POST request with invalid data
    response = client.post("/signup", data=data)

    # Assert expected error response code (e.g., 400 Bad Request)
    assert response.response == {"error": "Missing username, email, or password"}
    assert response.status_code == 400

    

    

