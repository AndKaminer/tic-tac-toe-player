class Board:

    def __init__(self, state=None):
        
        self.state: tuple[bool] = None
        self.board: list[list] = None
        self.p1turn: bool = None
        self.p1winner: bool = None

        if state != None and self.check_valid_state(state):
            self.state = state
        else:
            self.state = Board.get_empty_state()

        self.board = self.state_to_board()
        self.p1turn = self.calc_turn()
        self.p1winner = self.check_winner()
        if len(self.get_possible_moves()) == 0 or self.p1winner != None:
            self.game_finished = True
            self.p1winner = self.check_winner()
        else:
            self.game_finished = False

    def get_board(self) -> list[list]:
        return self.board

    def get_state(self) -> tuple:
        return self.state

    def get_p1turn(self) -> bool:
        return self.p1turn

    def get_p1winner(self) -> bool:
        return self.p1winner

    def get_game_finished(self) -> bool:
        return self.game_finished

    def check_valid_state(self, state: tuple) -> bool:
        try:
            for s in state:
                if s != None:
                    if type(s) != bool:
                        return False
        except Exception as e:
            return False

        return len(state) == 9

    def calc_turn(self) -> bool:
        x_count: int = 0
        y_count: int = 0

        for space in self.state:
            if space == True:
                x_count += 1
            elif space == False:
                y_count += 1

        return y_count >= x_count

    def check_winner(self) -> bool:
        state: tuple[bool] = self.state
        if not self.check_valid_state(state):
            raise Exception("Invalid state")

        for i in range(3):
            offset: int = i * 3
            if state[0 + offset] == state[1 + offset] == state[2 + offset]:
                # row check
                return state[0 + offset]
            elif state[0 + i] == state[3 + i] == state[6 + i]:
                # column check
                return state[0 + i]
            elif state[0] == state[4] == state[8]:
                # diag 1 check
                return state[0]
            elif state[2] == state[4] == state[6]:
                # diag 2 check
                return state[2]
        return None

    def state_to_board(self) -> list[list]:
        board: list[list] = Board.get_empty_board()
        state: tuple[bool] = self.get_state()
        if not self.check_valid_state(state):
            return board

        for i in range(3):
            for j in range(3):
                board[i][j] = state[(3 * i) + j]

        return board

    def board_to_state(self) -> tuple[bool]:
        board: list[list] = self.board
        intermediate: list = list(Board.get_empty_state())

        for i in range(9):
            col: int = i % 3
            row: int = i // 3
            intermediate[i] = board[row][col]

        return tuple(intermediate)

    def get_empty_board() -> list[list]:
        return [ [None] * 3 for i in range(3) ]

    def get_empty_state() -> tuple[bool]:
        return (None, None, None,
                None, None, None,
                None, None, None)

    def move(self, row: int, col: int):
        if type(row) != int or type(col) != int or row not in range(3) or col not in range(3):
            raise Exception("Invalid move")

        self.board[row][col] = self.p1turn
        self.state = self.board_to_state()

        self.p1winner = self.check_winner()
        self.p1turn = self.calc_turn()
        if len(self.get_possible_moves()) == 0 or self.p1winner != None:
            self.game_finished = True
            self.p1winner = self.check_winner()

    def reset(self) -> None:
        self.state = Board.get_empty_state()
        self.board = Board.get_empty_board()
        self.p1turn = None
        self.p1winner = None
        self.game_finished = False

    def get_possible_moves(self) -> list[tuple]:
        board: list[list] = self.get_board()
        output: list[tuple] = []

        for row in range(3):
            for col in range(3):
                if board[row][col] == None:
                    output.append((row, col))

        return output

    def get_possible_next_states(self) -> list[tuple]:
        '''
        Guaranteed to be same order as self.get_possible_moves
        '''
        possible_moves: list[tuple] = self.get_possible_moves()
        output: list[tuple] = []
        for row, col in possible_moves:
            idx: int = (3 * row) + col
            cur_state: list[bool] = list(self.get_state())
            cur_state[idx] = self.p1turn

            output.append(tuple(cur_state))

        return output

    def to_string(self) -> str:
        s: str = ""
        state: tuple[bool] = self.get_state()
        for i in range(9):
            if i % 3 == 0:
                s += '|'

            space: str = None
            if state[i] == True:
                space = 'X'
            elif state[i] == False:
                space = 'O'
            else:
                space = '_'

            s += space + '|'
            if i % 3 == 2:
                s += '\n'

        return s
        

def main():
    b = Board()

    b.move(0, 0)

    b.move(1, 0)

    b.move(1, 1)

    b.move(2, 1)

    print(b.to_string())
    print(b.get_p1winner())

    b.move(2, 2)

    print(b.to_string())
    print(b.get_p1winner())

if __name__ == '__main__':
    main()
