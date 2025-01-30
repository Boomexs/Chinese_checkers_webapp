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

    def set_id(self, index: int):
        self.id = index

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
        self.make_board()
        self.make_flat_array()
        self.connect_board()
        self.make_zones()
        self.player_pieces = {p: 0 for p in range(1, player_count + 1)}
        if player_count == 2:
            self.add_player('up',1)
            self.add_player('down',2)
            self.add_player('left_up',-1)
            self.add_player('left_down',-1)
            self.add_player('right_up',-1)
            self.add_player('right_down',-1)
            self.win_zones = {}
            self.win_zones[2] = 'up'
            self.win_zones[1] = 'down'
        if player_count == 3:
            self.add_player('up',1)
            self.add_player('down',0)
            self.add_player('left_up',0)
            self.add_player('left_down',2)
            self.add_player('right_up',0)
            self.add_player('right_down',3)
            self.win_zones = {}
            self.win_zones[1] = 'down' 
            self.win_zones[2] = 'right_up'
            self.win_zones[3] = 'left_up'
        if player_count == 4:
            self.add_player('up',-1)
            self.add_player('down',-1)
            self.add_player('left_up',1)
            self.add_player('left_down',2)
            self.add_player('right_down',3)
            self.add_player('right_up',4)
            self.win_zones = {}
            self.win_zones[1] = 'right_down' 
            self.win_zones[2] = 'left_up'
            self.win_zones[3] = 'right_up'
            self.win_zones[4] = 'left_down'
        if player_count == 6:
            self.add_player('up',1)
            self.add_player('left_up',2)
            self.add_player('left_down',3)
            self.add_player('down',4)
            self.add_player('right_up',5)
            self.add_player('right_down',6)
            self.win_zones = {}
            self.win_zones[1] = 'down'
            self.win_zones[2] =  'right_down' 
            self.win_zones[3] = 'right_up'
            self.win_zones[4] = 'up'
            self.win_zones[5] = 'left_down'
            self.win_zones[6] = 'left_up'
        self.selected = None

        return
    
    def make_board(self):
        self.board = []
        count = 0
        for row_count in STANDARD_BOARD:
            offset = row_count % 2
            place = 13 - ceil(row_count / 2) - floor(13/2) + offset
            # self.board.append([None] * place + [Board_node(0)] * row_count + [None] * place)
            self.board.append([None] * place + [Board_node(0) for _ in range(row_count)] + [None] * place)

    def connect_board(self):
        for i in range(len(self.board)-1):
            for j in range(len(self.board[i])):
                if self.board[i][j] is not None:
                    self.board[i][j].connect(right=self.board[i][j+1],left=self.board[i][j-1])
                    offset = i % 2
                    self.board[i][j].connect(down_right=self.board[i+1][j+offset])
                    self.board[i][j].connect(down_left=self.board[i+1][j-1+offset])

    def make_zones(self):
        self.zones = {}

        arr = []
        for i in range(0,4):
            for cell in self.board[i]:
                if cell is not None:
                    arr.append(cell)
        self.zones['up'] = arr.copy()


        arr = []
        for i in range(13,17):
            for cell in self.board[i]:
                if cell is not None:
                    arr.append(cell)
        self.zones['down'] = arr.copy()

        arr = get_first_non_none_elements(self.board[4],4)
        arr.extend(get_first_non_none_elements(self.board[5],3))
        arr.extend(get_first_non_none_elements(self.board[6],2))
        arr.extend(get_first_non_none_elements(self.board[7],1))
        self.zones['left_up'] = arr.copy()

        arr = get_last_non_none_elements(self.board[4],4)
        arr.extend(get_last_non_none_elements(self.board[5],3))
        arr.extend(get_last_non_none_elements(self.board[6],2))
        arr.extend(get_last_non_none_elements(self.board[7],1))
        self.zones['right_up'] = arr.copy()
        
        arr = get_first_non_none_elements(self.board[9],1)
        arr.extend(get_first_non_none_elements(self.board[10],2))
        arr.extend(get_first_non_none_elements(self.board[11],3))
        arr.extend(get_first_non_none_elements(self.board[12],4))
        self.zones['left_down'] = arr.copy()

        arr = get_last_non_none_elements(self.board[9],1)
        arr.extend(get_last_non_none_elements(self.board[10],2))
        arr.extend(get_last_non_none_elements(self.board[11],3))
        arr.extend(get_last_non_none_elements(self.board[12],4))
        self.zones['right_down'] = arr.copy()


    def add_player(self, where, p):
        for cell in self.zones[where]:
            cell.content = p
            self.player_pieces[p] = 10

    def decrease_player_pieces(self, p):
        if p in self.player_pieces:
            self.player_pieces[p] -= 1

    def make_flat_array(self):
        self.flatarr = [x for row in self.board for x in row if x is not None]
        for i in range(len(self.flatarr)):
            self.flatarr[i].set_id(i)


    def board_to_data(self):
        # Remove all None flatten to 1 dim array convert nodes to content
        to_send = [[int(x) for x in row if x is not None] for row in self.board]
        return to_send

    def board_to_full_data(self):
        to_send = [[{'id': x.id, 'content': int(x)} for x in row if x is not None] for row in self.board]
        return to_send
    
if(__name__ =='__main__'):
    test = Board(2)
    test.make_board()
    test.connect_board()
    test.board_to_data()

