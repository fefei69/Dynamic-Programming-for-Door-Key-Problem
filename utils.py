import os
import numpy as np
import gymnasium as gym
import pickle
import matplotlib.pyplot as plt
import imageio
import random
from minigrid.core.world_object import Goal, Key, Door

MF = 0  # Move Forward
TL = 1  # Turn Left
TR = 2  # Turn Right
PK = 3  # Pickup Key
UD = 4  # Unlock Door


def step_cost(action):
    # You should implement the stage cost by yourself
    # Feel free to use it or not
    # ************************************************
    return 5  # the cost of action


def step(env, action):
    """
    Take Action
    ----------------------------------
    actions:
        0 # Move forward (MF)
        1 # Turn left (TL)
        2 # Turn right (TR)
        3 # Pickup the key (PK)
        4 # Unlock the door (UD)
    """
    actions = {
        0: env.unwrapped.actions.forward,
        1: env.unwrapped.actions.left,
        2: env.unwrapped.actions.right,
        3: env.unwrapped.actions.pickup,
        4: env.unwrapped.actions.toggle,
    }

    (obs, reward, terminated, truncated, info) = env.step(actions[action])
    return step_cost(action), terminated


def generate_random_env(seed, task):
    """
    Generate a random environment for testing
    -----------------------------------------
    seed:
        A Positive Integer,
        the same seed always produces the same environment
    task:
        'MiniGrid-DoorKey-5x5-v0'
        'MiniGrid-DoorKey-6x6-v0'
        'MiniGrid-DoorKey-8x8-v0'
    """
    if seed < 0:
        seed = np.random.randint(50)
    env = gym.make(task, render_mode="rgb_array")
    env.reset(seed=seed)
    return env


def load_env(path):
    """
    Load Environments
    ---------------------------------------------
    Returns:
        gym-environment, info
    """
    with open(path, "rb") as f:
        env = pickle.load(f)

    info = {
        "height": env.unwrapped.height, 
        "width": env.unwrapped.width, 
        "init_agent_pos": env.unwrapped.agent_pos, 
        "init_agent_dir": env.unwrapped.dir_vec,
    }

    for i in range(env.unwrapped.height):
        for j in range(env.unwrapped.width):
            if isinstance(env.unwrapped.grid.get(j, i), Key):
                info["key_pos"] = np.array([j, i])
            elif isinstance(env.unwrapped.grid.get(j, i), Door):
                info["door_pos"] = np.array([j, i])
            elif isinstance(env.unwrapped.grid.get(j, i), Goal):
                info["goal_pos"] = np.array([j, i])

    return env, info


def load_random_env(env_folder):
    """
    Load a random DoorKey environment
    ---------------------------------------------
    Returns:
        gym-environment, info
    """
    env_list = [os.path.join(env_folder, env_file) for env_file in os.listdir(env_folder)]
    env_path = random.choice(env_list)
    with open(env_path, "rb") as f:
        env = pickle.load(f)

    info = {
        "height": env.unwrapped.height,
        "width": env.unwrapped.width,
        "init_agent_pos": env.unwrapped.agent_pos,
        "init_agent_dir": env.unwrapped.dir_vec,
        "door_pos": [],
        "door_open": [],
    }

    for i in range(env.unwrapped.height):
        for j in range(env.unwrapped.width):
            if isinstance(env.grid.get(j, i), Key):
                info["key_pos"] = np.array([j, i])
            elif isinstance(env.grid.get(j, i), Door):
                info["door_pos"].append(np.array([j, i]))
                if env.grid.get(j, i).is_open:
                    info["door_open"].append(True)
                else:
                    info["door_open"].append(False)
            elif isinstance(env.grid.get(j, i), Goal):
                info["goal_pos"] = np.array([j, i])

    return env, info, env_path


def save_env(env, path):
    with open(path, "wb") as f:
        pickle.dump(env, f)


def plot_env(env):
    """
    Plot current environment
    ----------------------------------
    """
    img = env.render()
    plt.figure()
    plt.imshow(img)
    plt.show()


def draw_gif_from_seq(seq, env_path, path="./gif/doorkey.gif"):
    """
    Save gif with a given action sequence
    ----------------------------------------
    seq:
        Action sequence, e.g [0,0,0,0] or [MF, MF, MF, MF]

    env:
        The doorkey environment
    """
    env, info = load_env(env_path)
    with imageio.get_writer(path, mode="I", duration=0.8) as writer:
        img = env.render()
        writer.append_data(img)
        for act in seq:
            step(env, act)
            img = env.render()
            writer.append_data(img)
    print(f"GIF is written to {path}")
    return None

def visualize_policy(env_path, policy, sleep=0.5, write_frames=False):
    import cv2
    import time
    env, info = load_env(env_path)
    for i, action in enumerate(policy):
        if write_frames==True:
            imageio.imwrite(f"starter_code/results/partB_frames/{env_path[-17:-4]}frame{i}.png", env.render())
        cost, _ = step(env, action)
        # print("Action: {}, Total Cost: {}".format(action, cost))
        if write_frames== True and i == len(policy)-1:
            imageio.imwrite(f"starter_code/results/partB_frames/{env_path[-17:-4]}frame_last.png", env.render())
        cv2.imshow("Env", cv2.resize(env.render(), (192*2, 192*2)))
        time.sleep(sleep) 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
def get_available_cells(env):
    """
    Get the available cells in the environment

    """
    available_cells = []
    for i in range(env.unwrapped.height):
        for j in range(env.unwrapped.width):
            if env.unwrapped.grid.get(j, i) is None:
                available_cells.append((j, i))
    return available_cells
    
def get_available_cells_partB():
    wall_cells = [(4,0),(4,1),(4,3),(4,4),(4,6),(4,7)]
    available_cells = []
    for i in range(8):
        for j in range(8):
            if (i,j) not in wall_cells:
                available_cells.append((i,j))
    return available_cells