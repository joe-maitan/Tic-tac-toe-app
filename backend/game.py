

class Game():
    board = None


    def __init__(self):
        self.board = ["","","","","","","","",""]

    def print_board(self):
        print(self.board)


    def make_move(self, player, position):
        return self.update_board(position, player)


    def update_board(self, position, player):
        if self.board[position] != "":
            raise Exception("Invalid move")
        else:
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

