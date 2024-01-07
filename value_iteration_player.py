from players import NonHumanPlayer
from board import Board

class ValueIterationPlayer(NonHumanPlayer):
    def __init__(self, board, max_delay:int=5):
        super().__init__(board, max_delay)
