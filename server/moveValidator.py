from __future__ import annotations
from abc import ABC, abstractmethod
from board import Board, Board_node
import copy


class MoveValidator:
    def __init__(self, game_strategy: GameStrategy):
        self._game_strategy = game_strategy

    #Straregy Setter
    def game_strategy(self, game_strategy: GameStrategy):
        self._game_strategy = game_strategy

    def possible_moves(self, board: Board, node_index: int, p: int):
        return self._game_strategy.possible_moves(board, node_index, p)


class GameStrategy(ABC):
    @abstractmethod
    def possible_moves(self, board: Board, node_index: int, p: int):
        pass


class GameStrategy1(GameStrategy):
    def try_jump(self, node: Board_node):
        if node.up_left is not None and node.up_left.content > 0:
            jump_node = node.up_left.up_left
            if jump_node is not None and jump_node.content == 0:
                jump_node.content = -2
                self.try_jump(jump_node)

        if node.up_right is not None and node.up_right.content > 0:
            jump_node = node.up_right.up_right
            if jump_node is not None and jump_node.content == 0:
                jump_node.content = -2
                self.try_jump(jump_node)

        if node.right is not None and node.right.content > 0:
            jump_node = node.right.right
            if jump_node is not None and jump_node.content == 0:
                jump_node.content = -2
                self.try_jump(jump_node)

        if node.left is not None and node.left.content > 0:
            jump_node = node.left.left
            if jump_node is not None and jump_node.content == 0:
                jump_node.content = -2
                self.try_jump(jump_node)

        if node.down_left is not None and node.down_left.content > 0:
            jump_node = node.down_left.down_left
            if jump_node is not None and jump_node.content == 0:
                jump_node.content = -2
                self.try_jump(jump_node)

        if node.down_right is not None and node.down_right.content > 0:
            jump_node = node.down_right.down_right
            if jump_node is not None and jump_node.content == 0:
                jump_node.content = -2
                self.try_jump(jump_node)

    def check_move_rec(self, node: Board_node):
        if node.up_left is not None:
            if node.up_left.content == 0:
                node.up_left.content = -2
                # check_move_rec(node.up_left)

        if node.up_right is not None:
            if node.up_right.content == 0:
                node.up_right.content = -2
                # check_move_rec(node.up_right)

        if node.right is not None:
            if node.right.content == 0:
                node.right.content = -2
                # check_move_rec(node.right)

        if node.left is not None:
            if node.left.content == 0:
                node.left.content = -2
                # check_move_rec(node.left)

        if node.down_left is not None:
            if node.down_left.content == 0:
                node.down_left.content = -2
                # check_move_rec(node.down_left)

        if node.down_right is not None:
            if node.down_right.content == 0:
                node.down_right.content = -2
                # check_move_rec(node.down_right)

        self.try_jump(node)

        return

    def possible_moves(self, board: Board, node_index: int, p: int):
        # print('possible moves start')
        node: Board_node
        # print(board.flatarr)
        node = board.flatarr[node_index]

        if node is None:
            return False

        if node.content != p:
            return False

        copy_of_board = copy.deepcopy(board)
        copy_of_node = copy_of_board.flatarr[node_index]
        self.check_move_rec(copy_of_node)

        board.selected = node

        return copy_of_board.board_to_data()


class GameStrategy2(GameStrategy):
    def check_move_rec(self, node: Board_node):
        if node.up_left is not None:
            node.up_left.content = -2
                # check_move_rec(node.up_left)

        if node.up_right is not None:
            node.up_right.content = -2
                # check_move_rec(node.up_right)

        if node.right is not None:
            node.right.content = -2
                # check_move_rec(node.right)

        if node.left is not None:
            node.left.content = -2
                # check_move_rec(node.left)

        if node.down_left is not None:
            node.down_left.content = -2
                # check_move_rec(node.down_left)

        if node.down_right is not None:
            node.down_right.content = -2
                # check_move_rec(node.down_right)

        return

    def possible_moves(self, board: Board, node_index: int, p: int):
        # print('possible moves start')
        node: Board_node
        # print(board.flatarr)
        node = board.flatarr[node_index]

        if node is None:
            return False

        if node.content != p:
            return False

        copy_of_board = copy.deepcopy(board)
        copy_of_node = copy_of_board.flatarr[node_index]
        self.check_move_rec(copy_of_node)

        board.selected = node

        return copy_of_board.board_to_data()