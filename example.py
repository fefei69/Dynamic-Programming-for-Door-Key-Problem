from utils import *
import cv2
import time
MF = 0  # Move Forward
TL = 1  # Turn Left
TR = 2  # Turn Right
PK = 3  # Pickup Key
UD = 4  # Unlock Door


def example_use_of_gym_env():
    """
    The Coordinate System:
        (0,0): Top Left Corner
        (x,y): x-th column and y-th row
    """

    print("<========== Example Usages ===========> ")
    env_path = "./starter_code/envs/example-8x8.env"
    # env, info = load_env(env_path) # load an environment

    env, info = load_env("starter_code/envs/known_envs/doorkey-5x5-normal.env")
    print("<Environment Info>\n")
    print(info)  # Map size
    # agent initial position & direction,
    # key position, door position, goal position
    print("<================>\n")

    # Visualize the environment
    plot_env(env)

    # Get the agent position
    agent_pos = env.get_wrapper_attr('agent_pos')

    # Get the agent direction
    agent_dir = env.get_wrapper_attr('dir_vec')  # or env.agent_dir 
    print("Agent Position: {}, Agent Direction: {}".format(agent_pos, agent_dir))
    # Get the cell in front of the agent
    front_cell = env.get_wrapper_attr('front_pos')  # == agent_pos + agent_dir 

    # Access the cell at coord: (2,3)
    cell = env.get_wrapper_attr('grid').get(2, 3)  # NoneType, Wall, Key, Goal

    # Get the door status
    door = env.get_wrapper_attr('grid').get(info["door_pos"][0], info["door_pos"][1])
    is_open = door.is_open
    is_locked = door.is_locked

    # Determine whether agent is carrying a key
    is_carrying = env.get_wrapper_attr('carrying') is not None

    policy = [MF, PK, TL, TL, MF, UD, MF, MF]

    for action in policy:
        cost, done = step(env, action)
        print("Action: {}, Cost: {}".format(action, cost))
        cv2.imshow("Env", env.render())
        time.sleep(0.5) 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    # Determine whether we stepped into the goal
    if done:
        print("Reached Goal")
        # print("Total Cost: {}".format(total)))

    # The number of steps so far
    print("Step Count: {}".format(env.get_wrapper_attr('step_count')))

if __name__ == "__main__":
    example_use_of_gym_env()
    

