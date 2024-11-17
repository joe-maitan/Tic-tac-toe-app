

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


    def print_board(self):
        print(self.board)

    
    def get_current_turn(self):
        return self.current_turn
    

    def switch_turn(self):
        if self.current_turn == self.player1['socketID']:
            self.current_turn = self.player2['socketID']
        else:
            self.current_turn = self.player1['socketID']


    def make_move(self, player, position):
        if self.board[position] != "":
            return "Invalid move"
        
        return self.update_board(position, player)


    def update_board(self, position, player):
        self.board[position] = player
        return self.check_winner(player)


    def check_winner(self, player):
        if (self.checkRows(player) or self.checkCols(player) or self.checkDiagonals(player)):
            return 'True'
        if "" not in self.board:
            return 'Draw'
        

    def checkRows(self, player):
        if self.board[0] == player and self.board[1] == player and self.board[2] == player:
            return True
        elif self.board[3] == player and self.board[4] == player and self.board[5] == player:
            return True
        elif self.board[6] == player and self.board[7] == player and self.board[8] == player:
            return True
        return False
    

    def checkCols(self, player):
        if self.board[0] == player and self.board[3] == player and self.board[6] == player:
            return True
        elif self.board[1] == player and self.board[4] == player and self.board[7] == player:
            return True
        elif self.board[2] == player and self.board[5] == player and self.board[8] == player:
            return True
        return False
    

    def checkDiagonals(self, player):
        if self.board[0] == player and self.board[4] == player and self.board[8] == player:
            return True
        elif self.board[2] == player and self.board[4] == player and self.board[6] == player:
            return True
        return False

