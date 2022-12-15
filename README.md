# Imki_Project
Technical test
Author : Florian Allender, PhD
***

## Dungeon Generator

The code generates dungeon maps of arbitrary size with an entrance (blue cell), an exit (red cell) and a treasure (yellow cell). The entrance is always the top left cell and the exit the bottom right. The treasure is placed randomly on the grid.

Two methods are available:
1. Depth First Search, that allows for an entirely new maze for each call.
2. Q-Learning generation, as described bellow.

The maze_generator.py file contains the classes Cell and Maze, allowing for cell (walls, keypoints) and maze (grid, dfs generation, neighbours search...) management.

![Dungeon example](https://myoctocat.com/assets/images/base-octocat.svg)

## Q-Learning approach

The algorithm starts with a nx*ny grid of cells where all the walls are up.
An agent is trained to generate mazes by searching the treasure and the exit, knocking down walls in the process.

Two steps are required: 
1. Train an agent to find the treasure and the exit. 
2. Use the trained agent to generate random maze.

Currently, the agent can create random mazes for a fixed position of the treasure. If the treasure is moved, the agent must be retrained.

The QLearning.py file contains the Agent class, allowing for action selection and q_table updating.





