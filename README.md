# Imki_Project
Technical test
***
Author : Florian Allender, PhD

## Dungeon Generator

The code generates dungeon maps of arbitrary size with an entrance, an exit and a treasure. The entrance is always the top left cell and the exit the bottom right. The treasure is placed randomly on the grid.

Two methods are available:
1. Depth First Search, that allows for an entirely new maze for each call.
2. Q-Learning generation, as described bellow.

## Q-Learning approach

The algorithm starts with a nx*ny grid of cells where all the walls are up.
An agent is trained to generate mazes by searching the treasure and the exit, knocking down walls in the process.

Two steps are required: 
1. Train an agent to find the treasure and the exit. 
2. Use the trained agent to generate random maze.

Currently, the agent can create random mazes for a fixed position of the treasure. If the treasure is moved, the agent must be retrained.


