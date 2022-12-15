# Technical test
Author : Florian Allender, PhD
***

## Dungeon Generator

The code generates dungeon maps of arbitrary size with an entrance (blue cell), an exit (red cell) and a treasure (yellow cell). The entrance is always the top left cell and the exit the bottom right. The treasure is placed randomly on the grid.

Two methods are available:
1. Depth First Search, that allows for an entirely new maze for each call.
2. Q-Learning generation, as described bellow.

The maze_generator.py file contains the classes Cell and Maze, allowing for cell (walls, keypoints) and maze (grid, dfs generation, neighbours search...) management.

![Dungeon example](https://github.com/AllFlorian/Imki_Project/blob/main/dungeon_test_0.svg)

## Q-Learning approach

The algorithm starts with a nx*ny grid of cells where all the walls are up.
An agent is trained to generate mazes by searching the treasure and the exit, knocking down walls in the process.

Two steps are required: 
1. Train an agent to find the treasure and the exit. 
2. Use the trained agent to generate random maze.

Currently, the agent can create random mazes for a fixed position of the treasure. If the treasure is moved, the agent must be retrained.

The QLearning.py file contains the Agent class, allowing for action selection and q_table updating during training.

## Requirements

* Python >= 3.7
* NumPy

## How to

Call python3 main.py with the relevant arguments.

optional arguments:
-  -h, --help,            show this help message and exit
-  --verbose VERBOSE, bool,     Print the training steps and save intermediate images
-  --height HEIGHT, int,       Dungeon grid height
-  --width WIDTH, int,         Dungeon grid width
-  --learning_rate LEARNING_RATE, float,
                        How quickly the algorithm tries to learn
-  --discount DISCOUNT, float,   Discount for estimated future action
-  --iterations ITERATIONS, int,
                        Iteration count
-  --method {dsf,qlearning},
                        Method to generate the dungeon
-  --mode {train,test},   Train or test the qlearing model
-  --to_generate TO_GENERATE, int,
                        Number of dungeons to generate
                        
The dungeons are saved as images in the svg format.
When using the QLearning algorithm, a qtable.txt file is generated after training. The file is then used when testing the agent.

Quick use with default arguments to generate 5 dungeons:
1. python3 main.py --mode train
2. python3 main.py --mode test

## Discussion

The agent needs to be retrained when the treasure is moved to an other location. The agent training could be improved so it could be able to find the treasure no matter its location, or the agent could place the treasure itself.

The training process uses information from the environment (valid neighbours) to knock down walls or not, mimicking the DFS algorithm. A different formalization of the problem (states, actions) could allow for a training without using information from the environement.

It is possible to evaluate the difficulty of a maze with two caracteristics:
1. possible directions to reach the exit. Only one direction (e.g. always "go right") is easier than two directions (e.g. always "go right" or "go down"), which is easier than all directions.
2. Presence of bifurcations. A maze with several accessible paths is more difficult to solve than a maze with only one path.

Those elements are sufficient to evaluate the difficulty of a maze if solved by a recursive algorithm such as DFS, since increasing the size or the number of bifurcations won't change the algorithmic difficulty. If solved by a human, the size and number of bifurcations play a more important role and should be included in the evaluation metric.

## References 

The codes used as basis for my own:

https://scipython.com/blog/making-a-maze/

https://github.com/valohai/qlearning-simple

## More results
![Dungeon 1](https://github.com/AllFlorian/Imki_Project/blob/main/dungeon_test_1.svg)
![Dungeon 2](https://github.com/AllFlorian/Imki_Project/blob/main/dungeon_test_2.svg)
![Dungeon 3](https://github.com/AllFlorian/Imki_Project/blob/main/dungeon_test_3.svg)
![Dungeon 4](https://github.com/AllFlorian/Imki_Project/blob/main/dungeon_test_4.svg)
