from utils import *
import cv2
import time
from tqdm import tqdm

MF = 0  # Move Forward
TL = 1  # Turn Left
TR = 2  # Turn Right
PK = 3  # Pickup Key
UD = 4  # Unlock Door

known_envs = ["doorkey-5x5-normal.env",
              "doorkey-6x6-direct.env",
              "doorkey-5x5-normal.env",
              "doorkey-6x6-normal.env",
              "doorkey-6x6-shortcut.env",
              "doorkey-8x8-normal.env",
              "doorkey-8x8-shortcut.env"]

unknown_envs = "DoorKey-8x8-1.env"
env_path = os.path.join("starter_code/envs/random_envs/", unknown_envs)
env, info = load_env(env_path)
# plot_env(env)
height, width = 8, 8
start_node = (3,5)
start_dir = (0,-1) # facing up
goal_node = [(5,1),(6,3),(5,6)] # 3 possible goal positions
key_node = [(1,1),(2,3),(1,6)] # 3 possible key positions
door_node = [(4,2),(4,5)] # 2 possible door positions
wall_cells = [(4,0),(4,1),(4,3),(4,4),(4,6),(4,7)]
available_cells = get_available_cells_partB()


key_pos = info['key_pos']
goal_pos = info['goal_pos']
door1 = env.get_wrapper_attr('grid').get(4, 2)
door2 = env.get_wrapper_attr('grid').get(4, 5)
door_1_status = door1.is_open
door_2_status = door2.is_open
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
    'door1_door2_locked': 0,
    'door1_door2_unlocked': 1,
    'door1_locked_door2_unlocked': 2,
    'door1_unlocked_door2_locked': 3
}

door_possible_positions = { 
    (4,2): 0,
    (4,5): 1
}
key_possible_positions = {
    (1,1): 0,
    (2,3): 1,
    (1,6): 2
}

goal_possible_positions = {
    (5,1): 0,
    (6,3): 1,
    (5,6): 2
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
        l = 0
    else:
        l = 1
    return l

def check_key(agent_dir, agent_pos, key_pos):
    agent_pos_front = (agent_pos[0] + agent_dir[0], agent_pos[1] + agent_dir[1]) 
    if agent_pos_front == (key_pos[0], key_pos[1]):
        return True
    return False

def check_door(agent_dir, agent_pos):
    # Check if there is a door in front of the agent 
    agent_pos_front = (agent_pos[0] + agent_dir[0], agent_pos[1] + agent_dir[1]) 
    if agent_pos_front == door_node[0]:
        return True, door_node[0]
    elif agent_pos_front == door_node[1]:
        return True, door_node[1]
    return False, None

def check_door_collision(agent_pos, door):
    if agent_pos in door_node and door == 0:
        return True
    elif agent_pos == door_node[0] and door == 2:
        return True
    elif agent_pos == door_node[1] and door == 3:
        return True
    return False

def get_door_status(door1_status, door2_status):
    if door1_status == True and door2_status == True:
        return 1
    elif door1_status == False and door2_status == False:
        return 0
    elif door1_status == False and door2_status == True:
        return 2
    elif door1_status == True and door2_status == False:
        return 3

def check_unlock_door(door, door_infront_pos):
    # check if the agent can unlock the door in front of it 
    if door == 0:
        return True
    elif door == 2 and door_infront_pos == door_node[0]:
        return True
    elif door == 3 and door_infront_pos == door_node[1]:
        return True
    return False

def motion_model(agent_dir, agent_pos, a, key, door, door_status_infront=None, key_status=False):
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
        if door_status_infront[0] == True and key == 1:
            new_agent_pos = agent_pos
            new_agent_dir = agent_dir
            # door1 and 2 are locked, unlocked door 1
            if door == 0 and door_status_infront[1] == door_node[0]:
                door = 3
            # door1 and 2 are locked, unlocked door 2
            elif door == 0 and door_status_infront[1] == door_node[1]:
                door = 2
            # door1 is locked, door2 is unlocked, unlocked door 1
            elif door == 2 and door_status_infront[1] == door_node[0]:
                door = 1
            # door2 is locked, door1 is unlocked, unlocked door 2
            elif door == 3 and door_status_infront[1] == door_node[1]:
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

# 36864 states
horizon = height*width*4*len(goal_node)*len(key_node)*4*2 - 1 
VALUE = np.ones((height, width, 4, 3, 3, 4, 2))*np.inf
POLICY = np.zeros((height, width, 4, 3, 3, 4, 2),dtype=str)
# initialize the value of goal state to 0
for gl in goal_node:
    VALUE[gl[0], gl[1], :, :, :, :, :] = 0
'''
states: pos_x, pos_y, headings id (0 ~ 3), goal position index (0 ~ 2) , key position index (0 ~ 2), door status of two doors (0 ~ 3), key_status (0 or 1)
'''
def main():
    for _ in tqdm(range(horizon)):
        OLDVALUE = VALUE.copy()
        # initialize the value of goal state to 0 at each time step
        for gl in goal_node:
            VALUE[gl[0], gl[1], :, :, :, :, :] = 0
        for i in range(height):
            for j in range(width):
                for heading in headings.keys():
                    for goal_pos in goal_node:
                        for key_pos in key_node:
                            for door_stats in door_status.keys():
                                for key_stats in key_status.keys():
                                    # current_state = (i, j, headings_to_index[f'{headings[heading]}'], key_pos, door_status[door_stats], key_status[key_stats])
                                    current_pos = (i, j)
                                    current_dir = headings[heading]
                                    # current_door = door_pos
                                    # current_key = key_pos
                                    # controls
                                    for u_key in actions.keys():
                                        new_agent_pos, new_agent_dir, key, door = motion_model((headings[heading][0], headings[heading][1]),
                                                                                                (i, j), 
                                                                                                u_key,
                                                                                                key_status[key_stats],
                                                                                                door_status[door_stats], 
                                                                                                door_status_infront=check_door(current_dir, current_pos),
                                                                                                key_status=check_key(current_dir, current_pos, key_pos))
                                        # skip if the agent cannot unlock the door in front of it
                                        if check_door(current_dir, current_pos)[0] == True and check_unlock_door(door_status[door_stats], check_door(current_dir, current_pos)[1]) == False and u_key == 'unlock_door':
                                            continue
                                        # change key and door status
                                        if new_agent_pos not in available_cells:
                                            continue
                                        # Can't move forward if there is a locked door
                                        if check_door_collision(new_agent_pos, door) == True:
                                            continue
                                        # print('new_agent_pos', new_agent_pos)
                                        # print('new_agent_dir', new_agent_dir)
                                        l = stage_cost(new_agent_dir, new_agent_pos)
                                        Q = VALUE[new_agent_pos[0], new_agent_pos[1], 
                                                    headings_to_index[f'{new_agent_dir}'], 
                                                    goal_possible_positions[goal_pos],
                                                    key_possible_positions[key_pos], 
                                                    door, 
                                                    key] + l
                                        
                                        if Q < VALUE[i, j, headings_to_index[f'{headings[heading]}'], goal_possible_positions[goal_pos], key_possible_positions[key_pos], door_status[door_stats], key_status[key_stats]] and Q != np.inf:
                                            VALUE[i, j, headings_to_index[f'{headings[heading]}'], goal_possible_positions[goal_pos], key_possible_positions[key_pos], door_status[door_stats], key_status[key_stats]] = Q
                                            POLICY[i, j, headings_to_index[f'{headings[heading]}'], goal_possible_positions[goal_pos], key_possible_positions[key_pos], door_status[door_stats], key_status[key_stats]] = actions[u_key]
                                            # if np.all(POLICY[start_node[0], start_node[1], headings_to_index[f'{(start_dir[0], start_dir[1])}'], :, :, :, 0] != ''):
                                            #     print("Policy found")
                                            #     return POLICY, VALUE
        if np.all(VALUE == OLDVALUE):
            print("Value function equals")
            return POLICY, VALUE
    return print("Policy not found")

if __name__ == "__main__":
    optimal_policy, optimal_value = main()

    # Visualize the policy
    # TODO: Find the policy for specific goal state and door status at start node 
    # Run the policy for 36 random environments
    for i in range(1, 36):
        fail = False
        new_agent_pos = start_node
        new_agent_dir = (start_dir[0], start_dir[1])
        unknown_envs = f"DoorKey-8x8-{i}.env"
        env_path = os.path.join("starter_code/envs/random_envs/", unknown_envs)
        env, info = load_env(env_path)
        # plot_env(env)
        door1, door2 = env.get_wrapper_attr('grid').get(4, 2), env.get_wrapper_attr('grid').get(4, 5)
        door_1_open, door_2_open = door1.is_open, door2.is_open
        
        key_pos = (info['key_pos'][0], info['key_pos'][1])
        goal_pos = (info['goal_pos'][0], info['goal_pos'][1])
        door = get_door_status(door_1_open, door_2_open)
        done = False
        key = 0
        optimal_path = []
        while done != True:
            action = POLICY[new_agent_pos[0], new_agent_pos[1], 
                            headings_to_index[f'{(new_agent_dir[0], new_agent_dir[1])}'], 
                            goal_possible_positions[goal_pos], 
                            key_possible_positions[key_pos], 
                            door, 
                            key]
            if action == '':
                print('Policy not found')
                done = True
                fail = True
                visualize_policy(env_path, optimal_path, sleep=0.1)
                # action = 1
                # import pdb; pdb.set_trace()
                continue
            optimal_path.append(int(action))
            print('Action:', action)
            new_agent_pos, new_agent_dir, key, door = motion_model(new_agent_dir, new_agent_pos, 
                                                                    inverse_actions[int(action)],
                                                                    key,
                                                                    door, 
                                                                    door_status_infront=check_door(new_agent_dir, new_agent_pos),
                                                                    key_status=check_key(new_agent_dir, new_agent_pos, key_pos))
            cost, done = step(env, int(action))
            # plot_env(env)
        # print('Optimal path:', optimal_path)
        # visualize_policy(env_path, optimal_path, sleep=1)
        # import pdb; pdb.set_trace()
        if fail == False:
            # visualize_policy(env_path, optimal_path, sleep=1)
            draw_gif_from_seq(optimal_path, env_path, path=os.path.join("starter_code/results/partB", f"{unknown_envs[:-4]}.gif"))

   
    