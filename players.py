from board import Board

from abc import ABC, abstractmethod
import random
import time

class Player(ABC):
    def __init__(self, board: Board):
        self.move_number: int = 0
        self.board: Board = board

    @abstractmethod
    def choose_move(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def move_semantics(self) -> tuple[int, int]:
        pass

    def move(self) -> None:
        row, col = self.move_semantics()

        self.board.move(row, col)

        self.move_number += 1

    def get_board(self) -> Board:
        return self.board

    def get_move_number(self) -> int:
        return self.move_number

    def reset(self) -> None:
        self.move_number = 0


class NonHumanPlayer(Player):
    def __init__(self, board: Board, max_delay: int):
        super().__init__(board)
        self.max_delay = max_delay

    def move_semantics(self) -> tuple[int, int]:
        delay: int = random.randint(0, self.max_delay)
        time.sleep(delay)
        return self.choose_move()
