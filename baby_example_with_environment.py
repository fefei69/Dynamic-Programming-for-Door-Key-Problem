from utils import *
import cv2
import time

class Node:
    def __init__(self, x, y, direction, cost, parent_index):
        self.x = x  # index of grid
        self.y = y  # index of grid
        self.cost = cost
        self.direction = direction
        self.parent_index = parent_index  # index of previous Node

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(
            self.cost) + "," + str(self.parent_index)
MF = 0  # Move Forward
TL = 1  # Turn Left
TR = 2  # Turn Right
PK = 3  # Pickup Key
UD = 4  # Unlock Door

env, info = load_env("starter_code/envs/known_envs/doorkey-5x5-test.env")
# plot_env(env)
height, width = info['height'], info['width']
start_node = info['init_agent_pos']
start_dir = info['init_agent_dir']
goal_node = info['goal_pos']
print("Environment Info: ", info)
# info[]
headings = ['L', 'R', 'U', 'D']

movement_map = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1),
    'D': (0, 1)
}

actions = {
    'forward': MF,  # No change in heading
    'turn_right': TR,
    'turn_left': TL
}
agent_dir = env.get_wrapper_attr('dir_vec')

# 2x2 grids
states = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
controls = np.array([[0, 1], [1, 0], [-1, 0], [0, -1]])
a = np.array([1, 1])
b = np.array([0, 0])
init_value_func = np.ones((1,8)) * np.inf
goal = np.array([1,1])
start = np.array([0,0])
print("init value function: ", init_value_func)
print(init_value_func.shape)
pol = np.zeros((7,8), dtype=str)
pol[0][0] = 'forward'
print(pol)
