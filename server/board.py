from abc import ABC, abstractmethod

#Interface for Board
class Board(ABC):
    @abstractmethod
    def create_board(self, players_amount: int):
        pass

    @abstractmethod
    def make_move(self, move: dict):
        pass

    @abstractmethod
    def check_win(self):
        pass


