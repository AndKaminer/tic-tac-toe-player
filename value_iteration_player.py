from utils import load_agent_value_function, gen_all_states
from players import NonHumanPlayer
from board import Board
from game import Game
from random_player import RandomPlayer

import random

class ValueIterationAgent:
    def __init__(self, discount_factor: float, player1: bool=True, load_file: str=None, epsilon: float=.05):
        if load_file:
            self.v_policy = load_agent_value_function(load_file)
        else:
            self.v_policy = { el : 0 for el in gen_all_states() }


        self.player1: bool = player1
        self.discount_factor: float = discount_factor
        self.epsilon: float = epsilon
        self.num_iters = 0

    def determine_reward(board: Board, player1: bool) -> int:
        reward: int = None
        if board.get_game_finished():
            winner: bool = board.get_p1winner()
            if winner == True:
                reward = 1
            elif winner == False:
                reward = -1
            else:
                return 0
        else:
            return 0

        return reward if player1 else -1 * reward

    def choose_move(self, state: tuple) -> tuple:
        b: Board = Board(state)
        moves: list[tuple] = b.get_possible_moves()
        states: list[tuple] = b.get_possible_next_states()

        move_reward: dict[tuple, float] = { moves[i] : self.v_policy[states[i]] for i in range(len(moves)) }
        return max(moves, key=lambda m : move_reward[m])        

    def upgrade_policy(self) -> None:
        v: dict[tuple, float] = { el : 0 for el in gen_all_states() }
        for state in v.keys():
            b = Board(state)
            reward: float = ValueIterationAgent.determine_reward(b, self.player1)
            possible_states: list[tuple] = b.get_possible_next_states()
            for s in possible_states:
                reward += (self.discount_factor * self.v_policy[s])
            v[state] = reward

        self.v_policy = v.copy()

    def train(self, epochs: int=10, iterations: int=100):
        for i in range(epochs):
            self.iteration(iterations)

        return self.get_win_rate()

    def iteration(self, n: int) -> float:
        for i in range(n):
            self.upgrade_policy()

    def get_win_rate(self) -> tuple[float, float]:
        win_count: int = 0
        wintie_count: int = 0
        b = Board()
        v_player: ValueIterationPlayer = ValueIterationPlayer(b, self, 0)
        r_player: RandomPlayer = RandomPlayer(b, 0)
        g = Game(v_player, r_player)

        for i in range(1000):
            states, winner = g.play(True)
            reward: int = ValueIterationAgent.determine_reward(b, True)
            if reward == 1:
                win_count += 1
                wintie_count += 1

            if reward == 0:
                wintie_count += 1

            g.reset()
            
        return (win_count / 1000, wintie_count / 1000)


class ValueIterationPlayer(NonHumanPlayer):
    def __init__(self, board: Board, agent: ValueIterationAgent=None, max_delay: int=5):
        super().__init__(board, max_delay)
        
        if agent:
            self.agent: ValueIterationAgent = agent
        else:
            v: ValueIterationAgent = ValueIterationAgent(.4)
            v.train(1, 10)
        self.board: Board = board

    def choose_move(self) -> tuple[int, int]:
        return self.agent.choose_move(self.board.get_state())
