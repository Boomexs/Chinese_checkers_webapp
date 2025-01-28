from board import Board, Board_node
import copy

def try_jump(node: Board_node):
    if node.up_left is not None and node.up_left.content > 0:
        jump_node = node.up_left.up_left
        if jump_node is not None and jump_node.content == 0:
            jump_node.content = -2
            try_jump(jump_node)

    if node.up_right is not None and node.up_right.content > 0:
        jump_node = node.up_right.up_right
        if jump_node is not None and jump_node.content == 0:
            jump_node.content = -2
            try_jump(jump_node)

    if node.right is not None and node.right.content > 0:
        jump_node = node.right.right
        if jump_node is not None and jump_node.content == 0:
            jump_node.content = -2
            try_jump(jump_node)

    if node.left is not None and node.left.content > 0:
        jump_node = node.left.left
        if jump_node is not None and jump_node.content == 0:
            jump_node.content = -2
            try_jump(jump_node)

    if node.down_left is not None and node.down_left.content > 0:
        jump_node = node.down_left.down_left
        if jump_node is not None and jump_node.content == 0:
            jump_node.content = -2
            try_jump(jump_node)

    if node.down_right is not None and node.down_right.content > 0:
        jump_node = node.down_right.down_right
        if jump_node is not None and jump_node.content == 0:
            jump_node.content = -2
            try_jump(jump_node)


def check_move_rec(node: Board_node):
    if node.up_left is not None:
        if node.up_left.content == 0:
            node.up_left.content = -2            

    if node.up_right is not None:
        if node.up_right.content == 0:
            node.up_right.content = -2

    if node.right is not None:
        if node.right.content == 0:
            node.right.content = -2

    if node.left is not None:
        if node.left.content == 0:
            node.left.content = -2

            
    if node.down_left is not None:
        if node.down_left.content == 0:
            node.down_left.content = -2


    if node.down_right is not None:
        if node.down_right.content == 0:
            node.down_right.content = -2

    try_jump(node)

    return


def possible_moves(board: Board, node_index: int, p: int):
    node: Board_node
    node = board.flatarr[node_index]

    if node is None:
        return False

    if node.content != p:
        return False

    copy_of_board = copy.deepcopy(board)
    copy_of_node = copy_of_board.flatarr[node_index]
    check_move_rec(copy_of_node)  
        
    board.selected = node

    return copy_of_board.board_to_data()

def check_for_win(board: Board, p: int):
    zone = board.zones[board.win_zones[p]]

    if None in zone:
        return False
    win_flag = False

    for cell in zone:
        if cell.content == p:
            win_flag = True
        elif cell.content == 0:
            return False
        
    return win_flag