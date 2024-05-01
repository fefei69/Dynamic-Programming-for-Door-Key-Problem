from utils import *
import cv2
import time


MF = 0  # Move Forward
TL = 1  # Turn Left
TR = 2  # Turn Right
PK = 3  # Pickup Key
UD = 4  # Unlock Door
known_envs = ["doorkey-5x5-normal.env",
              "doorkey-6x6-direct.env",
              "doorkey-6x6-normal.env",
              "doorkey-6x6-shortcut.env",
              "doorkey-8x8-normal.env",
              "doorkey-8x8-shortcut.env",
              "doorkey-8x8-direct.env"]

known_envs = known_envs[6]
env_path = os.path.join("starter_code/envs/known_envs/", known_envs)
env, info = load_env(env_path)
# plot_env(env)
height, width = info['height'], info['width']
start_node = info['init_agent_pos']
start_dir = info['init_agent_dir']
goal_node = info['goal_pos']
key_node = info['key_pos']
door_node = info['door_pos']
available_cells = get_available_cells(env)
# TODO: add key 
available_cells.append((goal_node[0],goal_node[1]))
available_cells.append((key_node[0],key_node[1]))
available_cells.append((door_node[0],door_node[1]))
# available_cells.remove((4,2))

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
    'turn_right': TR,
    'pickup_key': PK,
    'unlock_door': UD
}

inverse_actions = {
    MF: 'forward',
    TL: 'turn_left',
    TR: 'turn_right',
    PK: 'pickup_key',
    UD: 'unlock_door'
}

def stage_cost(agent_dir, agent_pos):
    if (agent_pos[0], agent_pos[1]) == start_node and agent_dir == (start_dir[0], start_dir[1]):
        print('start node found', agent_pos, agent_dir)
        l = 0
    else:
        l = 1
    return l

def check_key(agent_dir, agent_pos):
    agent_pos_front = (agent_pos[0] + agent_dir[0], agent_pos[1] + agent_dir[1]) 
    if agent_pos_front == (key_node[0], key_node[1]):
        return True
    return False

def check_door(agent_dir, agent_pos):
    agent_pos_front = (agent_pos[0] + agent_dir[0], agent_pos[1] + agent_dir[1]) 
    if agent_pos_front == (door_node[0], door_node[1]):
        return True
    return False

def motion_model(agent_dir, agent_pos, a, key, door, key_status=False, door_status=False):
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
    elif a == 'pickup_key':
        # There is a key in front of the agent
        if key_status == True:
            new_agent_pos = agent_pos
            new_agent_dir = agent_dir
            # key picked up 
            key = 1
        else:
            new_agent_pos = agent_pos
            new_agent_dir = agent_dir
            key = key
    elif a == 'unlock_door':
        # There is a door in front of the agent and the agent has a key
        if door_status == True and key == 1:
            new_agent_pos = agent_pos
            new_agent_dir = agent_dir
            # door unlocked
            door = 1
        else:
            new_agent_pos = agent_pos
            new_agent_dir = agent_dir
            door = door
        
    return new_agent_pos, new_agent_dir, key, door

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
horizon = height*width*4*2*2 - 1 
VALUE = np.ones((height, width, 4, 2, 2))*np.inf
POLICY = np.zeros((height, width, 4, 2, 2),dtype=str)
# initialize the value of goal state to 0
VALUE[goal_node[0], goal_node[1], :,:,:] = 0
'''
states: (pos_x, pos_y, headings id (0~4), door status (0 or 1), key_status (0 or 1)
'''
def main():
    # OLDVALUE = np.ones((5,5,4))*np.inf
    for _ in range(horizon):
        OLDVALUE = VALUE.copy()
        VALUE[goal_node[0], goal_node[1], :,:,:] = 0
        for i in range(height):
            for j in range(width):
                for heading in headings.keys():
                    for door_stats in door_status.keys():
                        for key_stats in key_status.keys():
                            # current_state = (i, j, headings_to_index[f'{headings[heading]}'], door_status[door_stats], key_status[key_stats])
                            current_pos = (i, j)
                            current_dir = headings[heading]
                            # controls
                            for u_key in actions.keys():
                                new_agent_pos, new_agent_dir, key, door = motion_model((headings[heading][0], headings[heading][1]),
                                                                                        (i, j), 
                                                                                        u_key,
                                                                                        key_status[key_stats],
                                                                                        door_status[door_stats], 
                                                                                        key_status=check_key(current_dir, current_pos), 
                                                                                        door_status=check_door(current_dir, current_pos))
                                # TODO: change key and door status
                                if new_agent_pos not in available_cells:
                                    continue
                                # Can't move forward if there is a locked door
                                if new_agent_pos == (door_node[0], door_node[1]) and door_status[door_stats] == 0:
                                    continue
                                # print('new_agent_pos', new_agent_pos)
                                # print('new_agent_dir', new_agent_dir)
                                l = stage_cost(new_agent_dir, new_agent_pos)
                                Q = VALUE[new_agent_pos[0], new_agent_pos[1], headings_to_index[f'{new_agent_dir}'], key, door] + l
                                
                                if Q < VALUE[i, j, headings_to_index[f'{headings[heading]}'], key_status[key_stats], door_status[door_stats]] and Q != np.inf:
                                    VALUE[i, j, headings_to_index[f'{headings[heading]}'], key_status[key_stats], door_status[door_stats]] = Q
                                    POLICY[i, j, headings_to_index[f'{headings[heading]}'], key_status[key_stats], door_status[door_stats]] = actions[u_key]
                                    # if POLICY[start_node[0], start_node[1], headings_to_index[f'{(start_dir[0], start_dir[1])}'],0,0] != '':
                                    #     import pdb; pdb.set_trace()
                                    #     print("Policy found")
                                    #     return POLICY, VALUE
        if np.all(VALUE == OLDVALUE):
            print("Value function equals")
            return POLICY, VALUE
    return print("Policy not found")

if __name__ == "__main__":
    # TODO: Loop over all known environments, check check how to utilize the value function as terminal condition
    optimal_policy, optimal_value = main()
    # Visualize the policy
    new_agent_pos = start_node
    new_agent_dir = (start_dir[0], start_dir[1])
    done = False
    key = 0
    door = 0
    optimal_path = []
    while done != True:
        action = POLICY[new_agent_pos[0], new_agent_pos[1], headings_to_index[f'{(new_agent_dir[0], new_agent_dir[1])}'], key, door]
        optimal_path.append(int(action))
        print('Action:', action)
        new_agent_pos, new_agent_dir, key, door = motion_model(new_agent_dir,
                                                                new_agent_pos, 
                                                                inverse_actions[int(action)],
                                                                key,
                                                                door, 
                                                                key_status=check_key(new_agent_dir, new_agent_pos), 
                                                                door_status=check_door(new_agent_dir, new_agent_pos))
        cost, done = step(env, int(action))
        # plot_env(env)
    print('Optimal path:', optimal_path)
    visualize_policy(env_path, optimal_path, sleep=1)
    # draw_gif_from_seq(optimal_path, env_path, path=os.path.join("starter_code/results/partA", f"{known_envs[:-4]}.gif"))