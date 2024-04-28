from utils import *
from example import example_use_of_gym_env

MF = 0  # Move Forward
TL = 1  # Turn Left
TR = 2  # Turn Right
PK = 3  # Pickup Key
UD = 4  # Unlock Door


def doorkey_problem(env, info):
    """
    You are required to find the optimal path in
        doorkey-5x5-normal.env
        doorkey-6x6-normal.env
        doorkey-8x8-normal.env

        doorkey-6x6-direct.env
        doorkey-8x8-direct.env

        doorkey-6x6-shortcut.env
        doorkey-8x8-shortcut.env

    Feel Free to modify this fuction
    """
    available_cells = get_available_cells(env)
    goal_pos = info["goal_pos"]
    print("<Environment Info>\n")
    print(info)  # Map size
    print("Goal Position: ", goal_pos)
    # Get the agent position
    agent_pos = env.get_wrapper_attr('agent_pos')
    # Get the agent direction
    agent_dir = env.get_wrapper_attr('dir_vec')  # or env.agent_dir 
    cost, done = step(env, TR)
    agent_dir = env.get_wrapper_attr('dir_vec')
    # Get the cell in front of the agent
    front_cell = env.get_wrapper_attr('front_pos')  # == agent_pos + agent_dir 

    # import pdb; pdb.set_trace()
    # Get the door status
    # door = env.get_wrapper_attr('grid').get(info["door_pos"][0], info["door_pos"][1])
    # is_open = door.is_open
    # is_locked = door.is_locked


    optim_act_seq = [MF, PK, TL, TL, MF, UD, MF, MF]#[TL, MF, PK, TL, UD, MF, MF, MF, MF, TR, MF]
    return optim_act_seq


def partA():
    env_path = "starter_code/envs/known_envs/doorkey-6x6-direct.env"
    env, info = load_env(env_path)  # load an environment
    seq = doorkey_problem(env,info)  # find the optimal action sequence
    # plot_env(env)  # visualize the environment
    visualize_policy(env, seq)  # visualize the policy
    # draw_gif_from_seq(seq, load_env(env_path)[0])  # draw a GIF & save


def partB():
    env_folder = "./envs/random_envs"
    env, info, env_path = load_random_env(env_folder)


if __name__ == "__main__":
    # example_use_of_gym_env()
    partA()
    # partB()

