from players import Player

class Game:
    def __init__(self, player1: Player, player2: Player):
        if player1.get_board() != player2.get_board():
            raise Exception("Players are playing on different boards!")

        self.player1: Player = player1
        self.player2: Player = player2
        self.board: Board = player1.get_board()

    def play(self, silent: bool=False) -> bool:
        while not self.board.get_game_finished():
            player: Player = self.player1 if self.board.get_p1turn() else self.player2
            self.move(player)

        if not silent:
            print(self.board.to_string())
        
        winner: bool = self.board.get_p1winner()

        if winner == None:
            print("Tie!")
        elif winner:
            print("P1 wins!")
        else:
            print("P2 wins!")

        return winner

    def move(self, player: Player, silent=True):
        player.move()

        if not silent:
            print(self.board.to_string())

    def reset(self) -> None:
        self.player1.reset()
        self.player2.reset()
        self.board.reset()
