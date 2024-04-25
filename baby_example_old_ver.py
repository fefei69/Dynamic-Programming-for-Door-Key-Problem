import numpy as np

class Map:
    def __init__(self, start, goal, xlim, ylim):
        self.start = start
        self.goal = goal
        self.xlim = xlim
        self.ylim = ylim
    def __str__(self) -> str:
        return "Start: " + str(self.start) + ", Goal: " + str(self.goal) + ", Xlim: " + str(self.xlim) + ", Ylim: " + str(self.ylim)
class Node:
    def __init__(self, x, y, cost, parent_index):
        self.x = x  # index of grid
        self.y = y  # index of grid
        self.cost = cost
        self.parent_index = parent_index  # index of previous Node

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(
            self.cost) + "," + str(self.parent_index)
#check out of bounds
def check_bounds(node):
    if node.x < 0 or node.x > 1:
        return False
    if node.y < 0 or node.y > 1:
        return False
    return True

def cal_index(node):
    return node.x*2+node.y # starting from 0

def get_optimal_poliy(optimal_states):
    optimal_policy = []
    for i in range(len(optimal_states)-1):
        diff = optimal_states[i+1] - optimal_states[i]
        # grab actions
        for key, value in actions.items():
            if np.allclose(value, diff):
                optimal_policy.append(key)
    return optimal_policy

def get_optimal_path(goal_node, closed_set):
    optimal_states = [np.array([goal_node.x, goal_node.y])]
    parent_index = goal_node.parent_index   
    while parent_index != -1:
        n = closed_set[parent_index]
        optimal_states.append(np.array([n.x, n.y]))
        parent_index = n.parent_index
    return optimal_states

# starting state
start = np.array([0,0])
# goal state
goal = np.array([1,1])
# states space 
states = np.array([[0,0],[0,1],[1,0],[1,1]])
controls = np.array([[0,1],[1,0],[-1,0],[0,-1]])

states = {str(states[i]):i for i in range(len(states))}
print(states)
actions = {'d':controls[0],'r':controls[1],'l':controls[2],'u':controls[3]}
inv_actions = {str(controls[0]):'d',str(controls[1]):'r',str(controls[2]):'l',str(controls[3]):'u'}
cost = np.array([1,1,1,1])


# Dynamic Programming
def DP(new_states, horizon):
    count = 0
    for t in range(horizon):
        for i, new_state in enumerate(new_states):
            # Terminate when horizon is reached
            if t == 7:
                return POLICY
            cost = np.array([1,1,1,1])

            # Terminate early when goal is reached
            if np.allclose(new_state, start):
                print("reach the goal!")
                return POLICY 
            
            # Set current parent state as goal
            goal = new_state
            # Get adjacent states
            new_states = goal + controls
            # Penalize the new state that go back to the last state
            if count > 0:
                goback_ind = np.where((controls==actions[POLICY[count-1][i]]).all(axis=1))
                cost[goback_ind] += 1000

            # check out of bounds states
            mask = (new_states > 1) | (new_states < 0)

            # set cost of start state to 0
            if np.where((new_states==start).all(axis=1)):
                cost[np.where((new_states==start).all(axis=1))] = 0

            idx = np.where(mask == True)[0]
            # Add large cost to invalid states
            cost[idx] += 1000
            min_cost = np.min(cost)
            low_cost_states = np.where(cost == min_cost)
            # randomly choose one state if there are multiple states with the same cost
            # low_cost_states = low_cost_states[0]
            new_states = new_states[low_cost_states]
            print("policy: ", controls[low_cost_states[0]])
            print("new states: ", new_states)
            if t == 0:
                for k, ind in enumerate(low_cost_states[0]):
                    s_id = states[f'{new_state}']
                    POLICY[t][s_id] = inv_actions[f'{controls[ind]}']
                if COST[t][s_id] == np.inf:
                    COST[t][s_id] = 0
                COST[t][s_id] += 1
            else:
                for _, ind in enumerate(low_cost_states[0]):
                    # global_cost[i] += cost[ind]
                    s_id = states[f'{new_state}']
                    POLICY[t][s_id] = inv_actions[f'{controls[ind]}']
                if COST[t][s_id] == np.inf:
                    COST[t][s_id] = 0
                COST[t][s_id] += 1
    return print("no solution!")


POLICY = np.zeros((3,4),dtype=str)
COST = np.ones((3,4))*np.inf
horizon = 3
p, c = DP([goal], horizon)
# print("Cost: ", costs)
print("Policy: ", p)
import pdb; pdb.set_trace()