##
# @file game.py
# 
# @brief Defines the game class.
# 
# This is the game class. It is a unique object created every time there is a new game!
# A game has a unique id, players, and board state. This is the object responsible for 
# keeping track of whose turn it is in the game.


class Game():
    game_id = None
    
    # for tracking game state
    player1 = {
        'username': None,
        'socketID': None,
        'symbol': None
    }

    player2 = {
        'username': None,
        'socketID': None,
        'symbol': None
    }

    current_turn = None  # socket ID of the player whose turn it is

    board = None

    # Game object constructor
    # @param game_id Unique identifier
    # @param player1 player1 of this game or the inviter
    # @param player2 player2 of this game or the invitee
    def __init__(self, game_id, player1, player2):
        self.game_id = game_id
        
        # player1 is always the inviter or 'X'
        self.player1['username'] = player1['username']
        self.player1['socketID'] = player1['socketID']
        self.player1['symbol'] = "X"

        # player2 is always the invitee or 'O'
        self.player2['username'] = player2['username']
        self.player2['socketID'] = player2['socketID']
        self.player2['symbol'] = "O"

        self.current_turn = player1['socketID']

        self.board = ["","","","","","","","",""]


    # print_board()
    # @param None
    # @brief Prints the board for that game object at the current state
    # @return None
    def print_board(self):
        print(self.board)


    # get_game_board()
    # @param None
    # @return The game board of that game at the current state
    def get_game_board(self):
        return self.board
    

    # reset_game_board()
    # @param None
    # @brief Resets that gameboard for that game object
    # @return None
    def reset_game_board(self):
        self.board = ["","","","","","","","",""]
    

    # get_current_turn()
    # @param None
    # @return Whose turn it is for that game
    def get_current_turn(self):
        return self.current_turn
    

    # switch_turn()
    # @param None
    # @brief Switches the current_turn variable in the Game object
    # @return None
    def switch_turn(self):
        if self.current_turn == self.player1['socketID']:
            self.current_turn = self.player2['socketID']
        else:
            self.current_turn = self.player1['socketID']


    # get_player_symbol(player)
    # @param player
    # @brief Checks to see which player has made a move, and fills that spot with their symbol
    # @return That player's symbol
    def get_player_symbol(self, player):
        if player == self.player1['username']:
            return self.player1['symbol']
        else:
            return self.player2['symbol']


    # make_move(player, position)
    # @param player who made the move
    # @param position that was picked on the board
    # @brief Check if the move is valid, if it is, call update board
    # @return board update
    def make_move(self, player, position):
        if self.board[position] != "":
            return "Invalid move"
        
        return self.update_board(position, player)


    # update_board(position, player)
    # @param position that was picked on the board
    # @param player who made a move
    # @brief updates the board with X or O depending on the player and position then calls check winner
    # @return check_winner results
    def update_board(self, position, player):
        self.board[position] = self.get_player_symbol(player)
        return self.check_winner(self.get_player_symbol(player))

    # check_winner(player)
    # @param player to check winning condition
    # @brief calls methods to check if there was a win in a row, column, or diagonal
    # @return True if player won, Draw if there was a draw
    def check_winner(self, player):
        if (self.checkRows(player) or self.checkCols(player) or self.checkDiagonals(player)):
            return 'True'
        if "" not in self.board:
            return 'Draw'
        
    # checkRows(player)
    # @param player to check winning condition
    # @brief checks all rows to see if player won
    # @return True if player won, False if not
    def checkRows(self, player):
        if self.board[0] == player and self.board[1] == player and self.board[2] == player:
            return True
        elif self.board[3] == player and self.board[4] == player and self.board[5] == player:
            return True
        elif self.board[6] == player and self.board[7] == player and self.board[8] == player:
            return True
        return False
    
    # checkCols(player)
    # @param player to check winning condition
    # @brief checks all columns to see if player won
    # @return True if player won, False if not
    def checkCols(self, player):
        if self.board[0] == player and self.board[3] == player and self.board[6] == player:
            return True
        elif self.board[1] == player and self.board[4] == player and self.board[7] == player:
            return True
        elif self.board[2] == player and self.board[5] == player and self.board[8] == player:
            return True
        return False
    
    # checkDiagonals(player)
    # @param player to check winning condition
    # @brief checks all diagonals to see if player won
    # @return True if player won, False if not
    def checkDiagonals(self, player):
        if self.board[0] == player and self.board[4] == player and self.board[8] == player:
            return True
        elif self.board[2] == player and self.board[4] == player and self.board[6] == player:
            return True
        return False

