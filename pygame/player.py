import numpy as np
from spider import *
from balls_mechanics import *

class Player_which_learns:
    
    def __init__(self, name, n, epsilon):
        # name = 0 or 1
        self.name = name    
        self.wins = 0
        self.losses = 0
        self.kernels = np.bool_(spider_flat(board=createboard(n)))
        self.n = n
        
        ### Epsilon-greedy algorithm
        # epsilon - a measure whether to choose exploration or exploitation
        self.epsilon = epsilon        
        # action:value dictionary, all possible boards without the full (n x n) one
        self.actions_values = np.zeros((2**n**2)-1)
        # learning parameters
        self.lr = 0.2
        self.discount_factor = 0.9
        
    def make_move(self, board):
        moves = list(possible_moves(board=board, kernels=self.kernels, n=self.n))
        values_for_moves = self.actions_values[moves]
        move_with_the_highest_value = moves[np.argmax(values_for_moves)]
        
        # 30 % exploration, 70 % exploitation
        if np.random.uniform(0, 1) <= self.epsilon:
            move = np.random.choice(moves)
        else:
            move = move_with_the_highest_value
        return move
    
    def reward_learning(self, reward, actions):
        for action in reversed(actions):
            self.actions_values[action] += self.lr * (self.discount_factor * reward - self.actions_values[action])
            reward = self.actions_values[action]