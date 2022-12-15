import argparse
import time
import maze_generator as mg
import QLearning as ql
import numpy as np

def main():

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', type=bool, default=False, help="Print the training steps and save intermediate images")
    parser.add_argument('--height', type=int, default=4, help="Dungeon grid height")
    parser.add_argument('--width', type=int, default=4, help="Dungeon grid width")
    parser.add_argument('--learning_rate', type=float, default=0.5, help='How quickly the algorithm tries to learn')
    parser.add_argument('--discount', type=float, default=0.98, help='Discount for estimated future action')
    parser.add_argument('--iterations', type=int, default=500, help='Iteration count')
    parser.add_argument('--method', type=str, choices=['dsf', 'qlearning'], default='qlearning', help="Method to generate the dungeon")
    parser.add_argument('--mode', type=str, choices=['train', 'test'], default='train', help="Train or test the qlearing model")
    parser.add_argument('--to_generate', type=int, default=5, help="Number of dungeon to generate")
    args, _ = parser.parse_known_args()


    nx, ny = args.width, args.height
    ix, iy = 0, 0

    if args.method == 'dsf':

        maze = mg.Maze(nx, ny, ix, iy)
        maze.write_svg('init.svg')
        maze.make_maze_dfs()

        print(maze)
        maze.write_svg('dungeon.svg')

    elif args.method == 'qlearning':

        if args.mode == "train":

            # setup simulation
            maze = mg.Maze(nx, ny, ix, iy)
            maze.write_svg('init.svg')
            total_reward = 0 # Score keeping
            last_total = 0

            qtable = np.zeros(shape=(nx,ny))
            agent = ql.Agent(maze, ix, iy, qtable)

            # main loop
            for step in range(args.iterations):
                old_state = agent.state # Store current state
                direction, next_cell, take_down = agent.get_next_action(old_state) # Query agent for the next action
                new_state, reward = agent.take_action(old_state, next_cell, direction, take_down) # Take action, get new state and reward
                agent.update(old_state, new_state, reward) # Let the agent update internals

                total_reward += reward # Keep score
                if step % 10 == 0 and args.verbose : # Print out metadata every 250th iteration
                    performance = (total_reward - last_total) / 250.0
                    print("Step : ", step, ", performance : ", performance, ", total reward : ", total_reward)
                    last_total = total_reward

                    maze.write_svg('dungeon{}.svg'.format(step))

                time.sleep(0.0001) # Avoid spamming stdout too fast!

            print("Final Q-table", agent.q_table)
            with open("qtable.txt", "w") as file:
                for line in agent.q_table:
                    for value in line:
                        file.write(str(value)+" ")
                    file.write('\n')

        if args.mode == "test" :

            try:
                with open('qtable.txt'): pass
            except IOError:
                print("The model must be trained first. Use the '--mode train' option.")

            qtable = []
            with open('qtable.txt', 'r') as file :
                values = file.read().split('\n')[:-1]
                for line in values:
                    qtable.append([float(value) for value in line.split(' ')[:-1]])
            maze = mg.Maze(nx, ny, ix, iy)
            agent = ql.Agent(maze, ix, iy, qtable)

            for n in range(args.to_generate):
                maze.rebuild()
                agent.reset()
                # same loop without updating the qtable
                for step in range(args.iterations):
                    old_state = agent.state # Store current state
                    direction, next_cell, take_down = agent.get_next_action(old_state) # Query agent for the next action
                    new_state, reward = agent.take_action(old_state, next_cell, direction, take_down) # Take action, get new state and reward

                    maze.write_svg('dungeon_test_{}.svg'.format(n))
            





if __name__ == "__main__":
    main()