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
# key_node = info['key_pos']
# door_node = info['door_pos']
print("Environment Info: ", info)
available_cells = get_available_cells(env)
# TODO: add key 
available_cells.append((goal_node[0],goal_node[1]))
# info[]

headings = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1),
    'D': (0, 1)
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
    'forward': MF,  # No change in heading
    'turn_left': TL,
    'turn_right': TR
    # 'pickup_key': PK,
    # 'unlock_door': UD
}
controls = {

    'forward': (0, 1),
    'turn_right': (1, 0),
    'turn_left': (-1, 0),
    'backward': (0, -1),
    '3': (0, 0),
    '4': (0, 0)
}

def motion_model(agent_dir, agent_pos):
    agent = []
    for a in actions:
        if a == 'forward':
            new_agent_pos = (agent_pos[0] + agent_dir[0], agent_pos[1] + agent_dir[1]) 
            agent.append(((new_agent_pos),(agent_dir),a))
        elif a == 'turn_left':
            if agent_dir==headings['L']:
                new_agent_dir = headings['D']
            elif agent_dir==headings['R']:
                new_agent_dir = headings['U']
            elif agent_dir==headings['U']:
                new_agent_dir = headings['L']
            elif agent_dir==headings['D']:
                new_agent_dir = headings['R']
            agent.append(((agent_pos),(new_agent_dir),a))
        elif a == 'turn_right':
            if agent_dir==headings['L']:
                new_agent_dir = headings['U']
            elif agent_dir==headings['R']:
                new_agent_dir = headings['D']
            elif agent_dir==headings['U']:
                new_agent_dir = headings['R']
            elif agent_dir==headings['D']:
                new_agent_dir = headings['L']
            agent.append(((agent_pos),(new_agent_dir),a))
        # elif a == 'pickup_key':
        #     agent.append(((agent_pos),(agent_dir)))
        # elif a == 'unlock_door':
        #     agent.append(((agent_pos),(agent_dir)))
    return agent

controls = np.array([[0, 1], [1, 0], [-1, 0], [0, -1], [0, 0]])
# generate all possible states
states = dict()
label = 0
for i in range(height):
    for j in range(width):
        for heading in headings.keys():
            states[(i, j), headings[heading]] = label
            label += 1
print(len(states))
goal = [((goal_node[0],goal_node[1]),(-1,0)), ((goal_node[0],goal_node[1]),(1,0)), ((goal_node[0],goal_node[1]),(0,-1)), ((goal_node[0],goal_node[1]),(0,1))]
horizon = 100 - 1
POLICY = np.zeros((horizon, horizon+1),dtype=str)
COST = np.ones((horizon, horizon+1))*np.inf
VALUE = np.ones(horizon+1)*np.inf
curr_state = [(key[0],key[1]) for key in states.keys()]
# initialize goal cost
for g in goal:
    g_dir = g[1]
    g_pos = g[0]
    state_index = states[g]
    VALUE[state_index] = 0

for t in range(50):
    Q = []
    Q_agent = []
    Q_policy = []
    for cur in curr_state:
        agents = motion_model(cur[1], cur[0])
        for u_id, agent in enumerate(agents):
            if agent[0] not in available_cells:
                continue
            Q.append(1 + VALUE[states[agent[0:2]]])
            Q_agent.append(agent[0:2])
            Q_policy.append(agent[2])
    min_Q = min(Q)
    min_index = np.where(np.array(Q) == min_Q)[0]
    print(type(min_index))
    Q_agent = [Q_agent[i] for i in min_index]
    Q_policy = [Q_policy[i] for i in min_index]
    OLD_VALUE = VALUE
    print(f"Value at time {t}: {VALUE, min_Q}")
    # update the value function, POLICY, COST
    for i in range(len(Q_agent)):
        print(states[Q_agent[i]])
        state_index = states[Q_agent[i]]
        VALUE[state_index] = min_Q
        POLICY[t][state_index] = actions[Q_policy[i]]
        COST[t][state_index] += 1
    # if np.allclose(OLD_VALUE, VALUE):
    #     print("finish")
    #     break
    curr_state = Q_agent
    import pdb; pdb.set_trace()

import pdb; pdb.set_trace()
for t in range(horizon):
    for g in goal:
        g_dir = g[1]
        g_pos = g[0]
        childs = motion_model(g_dir, g_pos)
        # only keep the child that is in the available cells
        for acts, child in enumerate(childs):
            state_index = states[child]
            POLICY[t][state_index] = f'{acts}'
            COST[t][state_index] = 1
            if child[0] not in available_cells:
                childs.remove(child)
                POLICY[t][state_index] = ''
                COST[t][state_index] = np.inf
            print(state_index)
    import pdb; pdb.set_trace()


# goal = [(key_node, -1, 0, 0, 1), (key_node, 1, 0, 0, 1), (key_node, 0, -1, 0, 1), (key_node, 0, 1, 0, 1)]
horizon = 400 - 1
POLICY = np.zeros((horizon, horizon+1),dtype=str)
COST = np.ones((horizon, horizon+1))*np.inf
start = (start_node, start_dir, 0, 0)
import pdb; pdb.set_trace()

