

class Game():

    # spaces = ["-" for _ in range(9)]
    board = None
    player1 = None
    player2 = None


    def __init__(self, player1, player2):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        # could also be a string of characters


    def print_board(self):
        print(self.board)


    def make_move(self, player, position):
        # where do they want to place their symbol?
        self.update_board(position, player)


    def update_board(self, position, player):
        # assumming position is a tuple (x, y)
        x = position[0]
        y = position[1]

        if self.board[x][y] is not None:
            raise Exception("Invalid move")
        else:
            pass
            self.board[x][y] = player.get_symbol()
            self.check_winner(player)


    def check_winner(self, player):
        if (self.checkRows(self, player) or self.checkCols(self, player) or self.checkDiagonals(self, player)):
            return True
        

    def checkRows(self, player):
        for row in self.board:
            if all([cell == player.get_symbol() for cell in row]):
                return True
        
        return False
    

    def checkCols(self, player):
        for i in range(0, 3, 1):
            for j in range(0, 3, 1):
                if self.board[j][i] != player.get_symbol():
                    break
                else:
                    return True
        
        return False
    

    def checkDiagonals(self, player):
        if self.board[0][0] == player.get_symbol() and self.board[1][1] == player.get_symbol() and self.board[2][2] == player.get_symbol():
            return True
        elif self.board[0][2] == player.get_symbol() and self.board[1][1] == player.get_symbol() and self.board[2][0] == player.get_symbol():
            return True
        else:
            return False
            

game = Game()
game.print_board()
