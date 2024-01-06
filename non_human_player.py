from player import Player
from board import Board

import random
import time

class NonHumanPlayer(Player):
    def __init__(self, board: Board, max_delay: int):
        super().__init__(board)
        self.max_delay = max_delay

    def move_semantics(self) -> tuple[int, int]:
        delay: int = random.randint(0, self.max_delay + 1)
        time.sleep(delay)

        return self.choose_move()

