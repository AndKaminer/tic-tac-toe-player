from players import NonHumanPlayer
from board import Board

import random

class RandomPlayer(NonHumanPlayer):
    def __init__(self, board: Board, max_delay: int=5):
        super().__init__(board, max_delay)

    def choose_move(self) -> tuple[int, int]:
        moves: list[tuple[int, int]] = self.board.get_possible_moves()

        if len(moves) == 0:
            raise Exception("No more moves to play!")
        
        return random.choice(moves)
