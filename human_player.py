from players import Player
from board import Board

class HumanPlayer(Player):
    def __init__(self, board: Board, terminal_control: bool=True):
        super().__init__(board)
        self.terminal_control = terminal_control

    def choose_move(self) -> tuple[int, int]:
        if self.terminal_control:
            print(self.board.to_string())
            
            while True:
                try:
                    row: int = int(input("Please choose a move. Type in the row (Zero indexed): "))
                    col: int = int(input("Pleaes choose a column. (Zero indexed): "))
                except Exception:
                    print("Invalid move. Please try again.")
                    continue

                if (row, col) not in self.board.get_possible_moves():
                    print("Move already taken")
                    continue

                break

            return (row, col)

    def move_semantics(self) -> tuple[int, int]:
        return self.choose_move()
