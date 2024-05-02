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

env, info = load_env("starter_code/envs/known_envs/doorkey-6x6-direct.env")
plot_env(env)
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
# available_cells = [(0,0),(0,1),(1,0),(1,1)]
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
    'forward': MF,  # No change in heading
    'turn_left': TL,
    'turn_right': TR
}

inverse_actions = {
    MF: 'forward',
    TL: 'turn_left',
    TR: 'turn_right'
}
controls = {

    'forward': (0, 1),
    'turn_right': (1, 0),
    'turn_left': (-1, 0),
    'backward': (0, -1),
    '3': (0, 0),
    '4': (0, 0)
}

def motion_model(agent_dir, agent_pos, a):
    if a == 'forward':
        new_agent_pos = (agent_pos[0] + agent_dir[0], agent_pos[1] + agent_dir[1]) 
        new_agent_dir = agent_dir
    elif a == 'turn_left':
        if agent_dir==headings['L']:
            new_agent_dir = headings['D']
        elif agent_dir==headings['R']:
            new_agent_dir = headings['U']
        elif agent_dir==headings['U']:
            new_agent_dir = headings['L']
        elif agent_dir==headings['D']:
            new_agent_dir = headings['R']
        new_agent_pos = agent_pos
    elif a == 'turn_right':
        if agent_dir==headings['L']:
            new_agent_dir = headings['U']
        elif agent_dir==headings['R']:
            new_agent_dir = headings['D']
        elif agent_dir==headings['U']:
            new_agent_dir = headings['R']
        elif agent_dir==headings['D']:
            new_agent_dir = headings['L']
        new_agent_pos = agent_pos
    return new_agent_pos, new_agent_dir

# Test motion model
# new_agent_pos = start_node
# new_agent_dir = (start_dir[0], start_dir[1])
# for u_key in actions.keys():
#     cost, done = step(env, actions[u_key])
#     new_agent_pos, new_agent_dir = motion_model(new_agent_dir, new_agent_pos, u_key)
#     print(new_agent_pos, new_agent_dir)
#     plot_env(env)
# import pdb; pdb.set_trace()

# 5x5x4 = 100 states
horizon = height*width - 1 
VALUE = np.ones((height,width,4))*np.inf
POLICY = np.zeros((height,width,4),dtype=str)
# initialize the value of goal state to 0
VALUE[goal_node[0], goal_node[1], :] = 0
def main():
    for _ in range(horizon):
        OLDVALUE = VALUE
        for i in range(height):
            for j in range(width):
                for heading in headings.keys():
                    # controls
                    for u_key in actions.keys():
                        new_agent_pos, new_agent_dir = motion_model((headings[heading][0], headings[heading][1]),(i, j), u_key)
                        if new_agent_pos not in available_cells:
                            continue
                        print('new_agent_pos', new_agent_pos)
                        print('new_agent_dir', new_agent_dir)
                        if (new_agent_pos[0], new_agent_pos[1]) == start_node and new_agent_dir == (start_dir[0], start_dir[1]):
                            print('start node found', new_agent_pos, new_agent_dir)
                            l = 0
                        else:
                            l = 1
                        Q = VALUE[new_agent_pos[0], new_agent_pos[1], headings_to_index[f'{new_agent_dir}']] + l
                        
                        if Q < VALUE[i, j, headings_to_index[f'{headings[heading]}']] and Q != np.inf:
                            VALUE[i, j, headings_to_index[f'{headings[heading]}']] = Q
                            POLICY[i, j, headings_to_index[f'{headings[heading]}']] = actions[u_key]
                            if POLICY[start_node[0], start_node[1], headings_to_index[f'{(start_dir[0], start_dir[1])}']] != '':
                                print("Policy found")
                                import pdb; pdb.set_trace()
                                return POLICY, VALUE
        if np.all(VALUE == OLDVALUE):
            print("Value function equals")
            import pdb; pdb.set_trace()
            # return POLICY, VALUE
    return print("Policy not found")


optimal_policy, optimal_value = main()
print(POLICY[start_node[0], start_node[1], headings_to_index[f'{(start_dir[0], start_dir[1])}']])
print(np.where(POLICY !=''))
print(POLICY[np.where(POLICY !='')])
# plot_env(env)
newagent_pos = start_node
newagent_dir = (start_dir[0], start_dir[1])
done = False
optimal_path = []
while done != True:
    action = POLICY[newagent_pos[0], newagent_pos[1], headings_to_index[f'{(newagent_dir[0], newagent_dir[1])}']]
    print('Action:', action)
    newagent_pos, newagent_dir = motion_model(newagent_dir, newagent_pos, inverse_actions[int(action)])
    cost, done = step(env, int(action))
    optimal_path.append(int(action))
    # plot_env(env)
visualize_policy("starter_code/envs/known_envs/doorkey-6x6-direct.env", optimal_path, sleep=1)