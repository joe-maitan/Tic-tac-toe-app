import pytest
from pymongo import MongoClient
from pytest_mock_resources import create_mongo_fixture

from flask import Flask
from config import app, db
from server import *
import game

player1 = {
    "username": "jjmaitan",
    "socketID": 5678
}
player2 = {
    "username": "erin",
    "socketID": 9012
}
default_game = game.Game(1234, player1, player2)


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

    logout_info = {
        "user_id": "bobbybiceps"
    }

    response = client.post('/signup', json=test_user_information)
    logout_reply = client.post('/logout', json=logout_info)
    assert response.status_code == 201
    assert response.json == {"message": "User created successfully"}
    assert logout_reply.json == {'message': 'bobbybiceps logged out successfully'}
    

def test_signup_missing_data(client, mock_db):
    test_user_information = {
        "email": "jjm@gmail.com",
        "password": "123456"
    }

    response = client.post('/signup', json=test_user_information)
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

    logout_info = {
        "user_id": "jjmaitan"
    }

    response = client.post('/login', json=test_login_information)
    logout_reply = client.post('/logout', json=logout_info)
    assert response.status_code == 201
    assert response.json == {"message": "jjmaitan logged in successfully"}
    assert logout_reply.json == {'message': 'jjmaitan logged out successfully'}
    

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

    logout_info = {
        "user_id": "jjmaitan"
    }

    client.post('/login', json=test_login_information)
    response = client.get('/profile')

    logout_reply = client.post('/logout', json=logout_info)
    assert response.status_code == 200
    assert response.json == {"user_id": "jjmaitan", "is_authenticated": True}
    assert logout_reply.json == {'message': 'jjmaitan logged out successfully'}


def test_get_active_users(client):
    joe_login_information = {
        "username": "jjmaitan",
        "password": "joePassword"
    }

    response = client.post('/login', json=joe_login_information)
    assert response.status_code == 201

    erin_login_information = {
        "username": "erin",
        "password": "1234"
    }

    response = client.post('/login', json=erin_login_information)
    assert response.status_code == 201

    response = client.get('/active_users')
    assert response.status_code == 200
    assert response.json == {"active_users": ["jjmaitan", "erin"]}


def test_game_constructor():
    assert default_game.game_id == 1234
    assert default_game.get_current_turn() == 5678
    assert default_game.board == ["","","","","","","","",""]
    assert default_game.player1['symbol'] == "X"
    assert default_game.player2['symbol'] == "O"

def test_empty_board_win_condition():
    assert default_game.check_winner(default_game.player1['symbol']) != 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'Draw'
    assert default_game.check_winner(default_game.player2['symbol']) != 'True'
    assert default_game.check_winner(default_game.player2['symbol']) != 'Draw'

def test_basic_make_move():
    default_game.make_move(player1['username'], 0)
    assert default_game.board == ["X","","","","","","","",""]
    assert default_game.check_winner(default_game.player1['symbol']) != 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'Draw'

def test_switch_turn():
    default_game.switch_turn()
    assert default_game.get_current_turn() == 9012

def test_complex_make_move():
    default_game.make_move(player2['username'], 8)
    assert default_game.board == ["X","","","","","","","","O"]
    default_game.switch_turn()
    default_game.make_move(player1['username'], 2)
    assert default_game.board == ["X","","X","","","","","","O"]
    default_game.switch_turn()
    default_game.make_move(player2['username'], 1)
    assert default_game.board == ["X","O","X","","","","","","O"]
    default_game.switch_turn()
    default_game.make_move(player1['username'], 3)
    assert default_game.board == ["X","O","X","X","","","","","O"]

def test_no_win_condition():
    assert default_game.board == ["X","O","X","X","","","","","O"]
    assert default_game.check_winner(default_game.player1['symbol']) != 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'Draw'
    assert default_game.check_winner(default_game.player2['symbol']) != 'True'
    assert default_game.check_winner(default_game.player2['symbol']) != 'Draw'

def test_first_col_win_condition():
    default_game.switch_turn()
    default_game.make_move(player2['username'], 7)
    assert default_game.board == ["X","O","X","X","","","","O","O"]
    default_game.switch_turn()
    assert default_game.make_move(player1['username'], 6)
    assert default_game.board == ["X","O","X","X","","","X","O","O"]
    assert default_game.check_winner(default_game.player1['symbol']) == 'True'
    assert default_game.check_winner(default_game.player2['symbol']) != 'True'
    assert default_game.check_winner(default_game.player2['symbol']) != 'Draw'

def test_invalid_move():
    assert default_game.make_move(player2['username'], 0) == 'Invalid move'
    assert default_game.board == ["X","O","X","X","","","X","O","O"]
    assert default_game.make_move(player1['username'], 8) == 'Invalid move'
    assert default_game.board == ["X","O","X","X","","","X","O","O"]
    assert default_game.make_move(player1['username'], 3) == 'Invalid move'
    assert default_game.board == ["X","O","X","X","","","X","O","O"]

def test_reset_board():
    default_game.reset_game_board()
    assert default_game.board == ["","","","","","","","",""]

def test_second_col_win_condition():
    default_game.make_move(player2['username'], 1)
    default_game.make_move(player2['username'], 4)
    default_game.make_move(player2['username'], 7)
    assert default_game.board == ["","O","","","O","","","O",""]
    assert default_game.check_winner(default_game.player2['symbol']) == 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'Draw'
    default_game.reset_game_board()

def test_third_col_win_condition():
    default_game.make_move(player1['username'], 2)
    default_game.make_move(player1['username'], 5)
    default_game.make_move(player1['username'], 8)
    assert default_game.board == ["","","X","","","X","","","X"]
    assert default_game.check_winner(default_game.player1['symbol']) == 'True'
    assert default_game.check_winner(default_game.player2['symbol']) != 'True'
    assert default_game.check_winner(default_game.player2['symbol']) != 'Draw'
    default_game.reset_game_board()

def test_first_row_win_condition():
    default_game.make_move(player2['username'], 0)
    default_game.make_move(player2['username'], 1)
    default_game.make_move(player2['username'], 2)
    assert default_game.board == ["O","O","O","","","","","",""]
    assert default_game.check_winner(default_game.player2['symbol']) == 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'Draw'
    default_game.reset_game_board()

def test_second_row_win_condition():
    default_game.make_move(player1['username'], 3)
    default_game.make_move(player1['username'], 4)
    default_game.make_move(player1['username'], 5)
    assert default_game.board == ["","","","X","X","X","","",""]
    assert default_game.check_winner(default_game.player1['symbol']) == 'True'
    assert default_game.check_winner(default_game.player2['symbol']) != 'True'
    assert default_game.check_winner(default_game.player2['symbol']) != 'Draw'
    default_game.reset_game_board()

def test_third_row_win_condition():
    default_game.make_move(player2['username'], 6)
    default_game.make_move(player2['username'], 7)
    default_game.make_move(player2['username'], 8)
    assert default_game.board == ["","","","","","","O","O","O"]
    assert default_game.check_winner(default_game.player2['symbol']) == 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'Draw'
    default_game.reset_game_board()

def test_backslash_diagonal_win_condition():
    default_game.make_move(player1['username'], 0)
    default_game.make_move(player1['username'], 4)
    default_game.make_move(player1['username'], 8)
    assert default_game.board == ["X","","","","X","","","","X"]
    assert default_game.check_winner(default_game.player1['symbol']) == 'True'
    assert default_game.check_winner(default_game.player2['symbol']) != 'True'
    assert default_game.check_winner(default_game.player2['symbol']) != 'Draw'
    default_game.reset_game_board()

def test_forwardslash_diagonal_win_condition():
    default_game.make_move(player2['username'], 2)
    default_game.make_move(player2['username'], 4)
    default_game.make_move(player2['username'], 6)
    assert default_game.board == ["","","O","","O","","O","",""]
    assert default_game.check_winner(default_game.player2['symbol']) == 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'True'
    assert default_game.check_winner(default_game.player1['symbol']) != 'Draw'
    default_game.reset_game_board()

def test_draw_win_condition():
    default_game.make_move(player1['username'], 0)
    default_game.make_move(player2['username'], 1)
    default_game.make_move(player1['username'], 2)
    default_game.make_move(player1['username'], 3)
    default_game.make_move(player2['username'], 4)
    default_game.make_move(player2['username'], 5)
    default_game.make_move(player2['username'], 6)
    default_game.make_move(player1['username'], 7)
    default_game.make_move(player1['username'], 8)
    assert default_game.board == ["X","O","X","X","O","O","O","X","X"]
    assert default_game.check_winner(default_game.player1['symbol']) == 'Draw'
    assert default_game.check_winner(default_game.player2['symbol']) == 'Draw'
    default_game.reset_game_board()