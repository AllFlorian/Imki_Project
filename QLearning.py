#https://github.com/valohai/qlearning-simple

import numpy as np
import random
import maze_generator as mg

class Agent:

    def __init__(self, maze, ix, iy, qtable, learning_rate=0.1, discount=0.5, exploration_rate=1.0, iterations=10000):
        
        self.q_table = qtable # Q-table for rewards accounting
        self.learning_rate = learning_rate # How much we appreciate new q-value over current
        self.discount = discount # How much we appreciate future reward over current
        self.exploration_rate = exploration_rate # Initial exploration rate
        self.exploration_delta = 1.0 / iterations # Shift from exploration to explotation

        self.maze = maze
        self.state = maze.cell_at(ix,iy)  # Start at beginning of the dungeon

    def get_next_action(self, state):
        if random.random() > self.exploration_rate: # Explore (gamble) or exploit (greedy)
            return self.greedy_action(state)
        else:
            return self.random_action(state)

    def get_reward(self, cell):
        if cell.treasure :
            return 50
        elif cell.exit :
            return 50
        else:
            return self.q_table[cell.x][cell.y]


    def greedy_action(self, state):
        # get valid neighbours
        neighbours = self.maze.find_valid_neighbours(state)
        take_down = True
        
        if neighbours == []:
            take_down = False
            neighbours = self.maze.find_valid_neighbours(state, valid=False)
            direction, next_cell = random.choice(neighbours)
        else:
            # check rewards
            rewards = []
            for _, cell in neighbours:
                rewards.append(self.get_reward(cell))  
            choice = np.random.choice(np.where(rewards == np.amax(rewards))[0])
            direction, next_cell = neighbours[choice]

        return direction, next_cell, take_down

    def random_action(self, state):
        take_down = True
        # get valid neighbours
        neighbours = self.maze.find_valid_neighbours(state)
        if neighbours == []:
            take_down = False
            neighbours = self.maze.find_valid_neighbours(state, valid=False)
            direction, next_cell = random.choice(neighbours)
        else:
            # choose a neighbour at random
            direction, next_cell = random.choice(neighbours)

        return direction, next_cell, take_down

    def take_action(self, cell, next_cell, direction, take_down):


        if take_down:
            cell.knock_down_wall(next_cell, direction)
        reward = self.get_reward(next_cell)

        self.state = next_cell

        return self.state, reward

    def update(self, old_state, new_state, reward):
        # Old Q-table value
        old_value = self.q_table[old_state.x][old_state.y]
        # What would be our best next action?
        _, future_action, _ = self.greedy_action(new_state)
        # What is reward for the best next action?
        future_reward = self.get_reward(future_action)

        # Main Q-table updating algorithm
        new_value = old_value + self.learning_rate * (reward + self.discount * future_reward - old_value)
        self.q_table[old_state.x][old_state.y] = new_value

        # Finally shift our exploration_rate toward zero (less gambling)
        if self.exploration_rate > 0:
            self.exploration_rate -= self.exploration_delta

    def reset(self):
        self.state = self.maze.cell_at(0,0)  # Reset state the beginning of dungeon
        return self.state