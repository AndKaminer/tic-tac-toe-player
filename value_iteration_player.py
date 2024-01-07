from utils import load_agent_value_function, gen_all_states
from players import NonHumanPlayer
from board import Board
from game import Game
from random_player import RandomPlayer

import random

class ValueIterationAgent:
    def __init__(self, board: Board, discount_factor: float, player1: bool=True, load_file: str=None, epsilon: float=.05):
        if load_file:
            self.v_policy = load_agent_value_function(load_file)
        else:
            self.v_policy = { el : 0 for el in gen_all_states() }

        self.v = self.v_policy.copy()

        self.board: Board = board
        self.player1: bool = player1
        self.discount_factor: float = discount_factor
        self.epsilon: float = epsilon
        self.num_iters = 0

    def determine_reward(self) -> int:
        reward: int = None
        if self.board.get_game_finished():
            winner: bool = self.board.get_p1winner()
            if winner == True:
                reward = 1
            elif winner == False:
                reward = -1
            else:
                return 0
        else:
            return 0

        return reward if self.player1 else -1 * reward

    def update_v(self, states: list[tuple], reward: int):
        for i in range(len(states) - 1, -1, -2): # don't reward initial state
            state: tuple = states[i]
            discount: float = pow(self.discount_factor, i)
            self.v[state] += discount * reward

    def choose(self, full_greedy=False) -> tuple[int, int]:
        possible_states: list[tuple] = self.board.get_possible_next_states()
        possible_moves: list[tuple] = self.board.get_possible_moves()
        move: tuple[int, int] = None
        if random.random() <= self.epsilon:
            move = random.choice(possible_moves)
        else:
            value_mapping: dict[tuple, float] = {} # move : value
            for i in range(len(possible_states)):
                state: tuple[bool] = possible_states[i]
                move: tuple[int, int] = possible_moves[i]
                value: float = self.v_policy[state]
                value_mapping[move] = value

            move = max(value_mapping.keys(), key=lambda k : value_mapping[k])
        return move

    def iteration(self, n: int) -> None:
        v1: ValueIterationPlayer = ValueIterationPlayer(self.board, self, 0)
        r2: RandomPlayer = RandomPlayer(self.board, 0)
        g: Game = Game(v1, r2)

        for i in range(n):
            states: list[tuple] = None
            winner: bool = None
            states, winner = g.play(silent=True)
            reward: int = self.determine_reward()
            self.update_v(states, reward)
            g.reset()

        self.v_policy = self.v.copy()

    def epoch(self, n: int, size: int=1000):
        for i in range(n):
            print(f"Epoch: {i}")
            self.iteration(size)


class ValueIterationPlayer(NonHumanPlayer):
    def __init__(self, board: Board, agent: ValueIterationAgent, max_delay: int=5):
        super().__init__(board, max_delay)
        self.agent: ValueIterationAgent = agent

    def choose_move(self) -> tuple[int, int]:
        return self.agent.choose()
