# Works well for grids version with only translations no headings
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

# plot_env(env)
height, width = 3,3#info['height'], info['width']
start_node = (0,0)#info['init_agent_pos']
goal_node = (1,2)#info['goal_pos']
# key_node = info['key_pos']
# door_node = info['door_pos']
# available_cells = get_available_cells(env)
# TODO: add key 
# available_cells.append((goal_node[0],goal_node[1]))
available_cells = [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1),(0,2),(1,2),(2,2)]
# info[]

headings = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1),
    'D': (0, 1)
}

headings_to_index = {
    '(-1, 0)': 0,
    '(1, 0)' : 1,
    '(0, -1)': 2,
    '(0, 1)' : 3
}

door_status = {
    'locked': 0,
    'unlocked': 1
}

key_status = {
    'not_picked': 0,
    'picked': 1
}

actions = {
    'l': 1,
    'r': 2,
    'u': 3,
    'd': 4
}



def motion_model(agent_pos, a):
    if a == 'u':
        new_agent_pos = (agent_pos[0] , agent_pos[1] + 1) 
    elif a == 'l':
        new_agent_pos = (agent_pos[0] - 1, agent_pos[1]) 
    elif a == 'r':
        new_agent_pos = (agent_pos[0] + 1, agent_pos[1])
    elif a == 'd':
        new_agent_pos = (agent_pos[0] , agent_pos[1] - 1)
    return new_agent_pos

# 5x5x4 = 100 states
horizon = height*width - 1
VALUE = np.ones((height,width))*np.inf
POLICY = np.zeros((height,width),dtype=str)
# initialize the value of goal state to 0
VALUE[goal_node[0], goal_node[1]] = 0
# generate all possible states
def main():
    for _ in range(horizon):
        OLDVALUE = VALUE
        for i in range(height):
            for j in range(width):
                # controls
                for u_key in actions.keys():
                    new_agent_pos = motion_model((i, j), u_key)
                    if new_agent_pos not in available_cells:
                        continue
                    print('new_agent_pos', new_agent_pos)
                    if (new_agent_pos[0], new_agent_pos[1]) == start_node :
                        print('start node found', new_agent_pos)
                        l = 0
                    else:
                        l = 1
                    Q = VALUE[new_agent_pos[0], new_agent_pos[1]] + l
                    
                    if Q < VALUE[i, j] and Q != np.inf:
                        print('Q', Q)
                        VALUE[i, j] = Q
                        POLICY[i, j] = u_key
                        if POLICY[start_node[0], start_node[1]] != '':
                            print("Policy found")
                            return POLICY, VALUE
        if np.all(VALUE == OLDVALUE):
            print("Value function equals")
            import pdb; pdb.set_trace()
            return POLICY, VALUE
        # OLDVALUE = VALUE 
    return print("Policy not found")
optimal_policy, optimal_value = main()
print(np.where(POLICY !=''))
print(POLICY[np.where(POLICY !='')])
newagent = start_node
while POLICY[newagent[0], newagent[1]] != '':
    newagent = motion_model((newagent[0], newagent[1]),POLICY[newagent[0], newagent[1]])
    print(newagent)
