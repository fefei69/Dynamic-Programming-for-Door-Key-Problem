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
actions = {'down':controls[0],'right':controls[1],'left':controls[2],'up':controls[3]}

global_policy = []
global_cost = []
start_node = Node(1, 0, 0, -1)
goal_node = Node(1, 1, 0, -1)
open_set, closed_set = dict(), dict()
open_set[cal_index(goal_node)] = goal_node

# planning 
while True:
    c_id = min(open_set, key=lambda o: open_set[o].cost)
    current = open_set[c_id]

    # check if the current node is the goal
    if current.x == start_node.x and current.y == start_node.y:
        print("Find goal")
        start_node.parent_index = current.parent_index
        start_node.cost = current.cost
        break
    # Remove the item from the open set
    del open_set[c_id]

    # Add it to the closed set
    closed_set[c_id] = current
    # expand search to current node's neighbors (search childs)
    for u in controls:
        node = Node(current.x + u[0], current.y + u[1], current.cost + 1, c_id)
        node_id = cal_index(node)
        # if the node is already in the closed set, skip it (going backwards)
        if node_id in closed_set:
            continue
        # add large cost to invalid states
        if not check_bounds(node):
            node.cost += 1000

        if node_id not in open_set:
            open_set[node_id] = node  # Discover a new node
        else:
            if open_set[node_id].cost >= node.cost:
                # This path is the best until now. record it!
                open_set[node_id] = node
    print("running...")
optim_nodes = get_optimal_path(start_node, closed_set)
optim_policy = get_optimal_poliy(optim_nodes)
print("Start Node: ", start_node.x, start_node.y)
print("Goal Node: ", goal_node.x, goal_node.y)
print("Optimal Nodes: ", optim_nodes)
print("Optimal Policy from start: ", optim_policy)