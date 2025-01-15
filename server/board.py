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

def get_first_non_none_elements(arr, length):
    result = []
    for item in arr:
        if item is not None:
            result.append(item)
        if len(result) == length:
            break
    # print(f"result: {result}")
    return result

def get_last_non_none_elements(arr, length):
    result = []
    for item in reversed(arr):
        if item is not None:
            result.append(item)
        if len(result) == length:
            break
    return result[::-1]  

class Board_node():
    def __init__(self, content: int):
        self.up_left: Board_node = None
        self.up_right: Board_node = None
        self.left: Board_node = None
        self.right: Board_node = None
        self.down_left: Board_node = None
        self.down_right: Board_node = None
        self.content: int = content
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
    
    def __int__(self):
        return self.content
    
    def __repr__(self):
        return str(self.content)



class Board():
    def __init__(self, player_count: int):
        self.player_count = player_count
        self.moves = []
        return
    
    def make_board(self):
        self.board = []
        for row_count in STANDARD_BOARD:
            place = 13 - floor(row_count / 2) - floor(13/2)
            # self.board.append([None] * place + [Board_node(0)] * row_count + [None] * place)
            self.board.append([None] * place + [Board_node(0) for _ in range(row_count)] + [None] * place)

    def connect_board(self):
        for i in range(len(self.board)-1):
            for j in range(len(self.board[i])):
                if self.board[i][j] is None:
                    continue
                self.board[i][j].connect(down_left=self.board[i+1][j-1],down_right=self.board[i+1][j])

    def add_player(self, where: str, p: int):
        # Where
        # 1 == up 2 == down
        if(where == 'up'):
            for i in range(0,4):
                for cell in self.board[i]:
                    if cell is not None:
                        cell.content = p
        if(where == 'down'):
            for i in range(13,17):
                for cell in self.board[i]:
                    if cell is not None:
                        cell.content = p
        if(where == 'left_up'):
            arr = get_first_non_none_elements(self.board[4],4)
            arr.extend(get_first_non_none_elements(self.board[5],3))
            arr.extend(get_first_non_none_elements(self.board[6],2))
            arr.extend(get_first_non_none_elements(self.board[7],1))
            for cell in arr:
                cell.content = p
        if(where == 'right_up'):
            arr = get_last_non_none_elements(self.board[4],4)
            arr.extend(get_last_non_none_elements(self.board[5],3))
            arr.extend(get_last_non_none_elements(self.board[6],2))
            arr.extend(get_last_non_none_elements(self.board[7],1))
            for cell in arr:
                cell.content = p
        if(where == 'left_down'):
            arr = get_first_non_none_elements(self.board[9],1)
            arr.extend(get_first_non_none_elements(self.board[10],2))
            arr.extend(get_first_non_none_elements(self.board[11],3))
            arr.extend(get_first_non_none_elements(self.board[12],4))
            for cell in arr:
                cell.content = p
        if(where == 'right_down'):
            arr = get_last_non_none_elements(self.board[9],1)
            arr.extend(get_last_non_none_elements(self.board[10],2))
            arr.extend(get_last_non_none_elements(self.board[11],3))
            arr.extend(get_last_non_none_elements(self.board[12],4))
            for cell in arr:
                cell.content = p
    def board_to_data(self):
        # Remove all None flatten to 1 dim array convert nodes to content
        to_send = [[int(x) for x in row if x is not None] for row in self.board]
        return to_send
    
if(__name__ =='__main__'):
    test = Board(2)
    test.make_board()
    test.connect_board()
    test.board_to_data()
