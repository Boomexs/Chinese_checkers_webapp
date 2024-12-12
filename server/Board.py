from math import floor, ceil

STANDARD_BOARD = [
    1,
    2,
    3,
    4,
    13,
    12,
    11,
    10,
    9,
    10,
    11,
    12,
    13,
    4,
    3,
    2,
    1,
]

def mid_odd(number: int) -> int:
    return floor(number/2)

def mid_left_even(number: int) -> int:
    return floor(number/2)

def mid_right_even(number: int) -> int:
    return floor(number/2) + 1

class Board_node():
    def __init__(self):
        self.up_left: Board_node = None
        self.up_right: Board_node = None
        self.left: Board_node = None
        self.right: Board_node = None
        self.down_left: Board_node = None
        self.down_right: Board_node = None
        return
    
    def connect(self, up_left: 'Board_node' = None,up_right: 'Board_node' = None,left: 'Board_node' = None,right: 'Board_node' = None,down_left: 'Board_node' = None,down_right: 'Board_node' = None):
        if(up_left is not None):
            self.up_left = up_left
            self.up_left.down_right = self
        if(up_right is not None):
            self.up_right = up_right
            self.up_right.down_left = self
        if(left is not None):
            self.left = left
            self.left.right = self
        if(right is not None):
            self.right = right
            self.right.left = right
        if(down_left is not None):
            self.down_left = down_left
            self.down_left.up_right = self
        if(down_right is not None):
            self.down_right = down_right
            self.down_right.up_left = self

    def __str__(self):
        return 'node'
    
    def __repr__(self):
        return "####"



class Board():
    def __init__(self, player_count: int):
        self.player_count = player_count
        self.moves = []
        if(self.player_count == 2):
            self.piece_count = 15
        elif(self.player_count > 2 and self.player_count <= 6):
            self.piece_count = 10
        return
    
    def make_board(self):
        self.board = []
        for row_count in STANDARD_BOARD:
            place = 13 - floor(row_count / 2) - floor(13/2)
            self.board.append([None] * place + [Board_node()] * row_count + [None] * place)
        # for i in range(len(self.board)):
        #     if i % 2 == 1:
        #         print(' ',self.board[i])
        #     else:
        #         print(self.board[i])
        # return

    def connect_board(self):
        for i in range(len(self.board)-1):
            for j in range(len(self.board[i])):
                if self.board[i][j] is None:
                    continue
                self.board[i][j].connect(down_left=self.board[i+1][j-1],down_right=self.board[i+1][j])
    
if(__name__ =='__main__'):
    test = Board(2)
    test.make_board()
    test.connect_board()
