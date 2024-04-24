import numpy as np

#check out of bounds
def check_bounds(state):
    if state[0] < 0 or state[0] > 1:
        return False
    if state[1] < 0 or state[1] > 1:
        return False
    return True

# starting state
start = np.array([0,0])
# goal state
goal = np.array([3,1])
# states space 
states = np.array([[0,0],[0,1],[1,0],[1,1]])
controls = np.array([[0,1],[1,0],[-1,0],[0,-1]])
actions = {'down':controls[0],'right':controls[1],'left':controls[2],'up':controls[3]}
cost = np.array([1,1,1,1])


# Dynamic Programming
def DP(new_states_, policy=[], count=0):
    for i, new_state in enumerate(new_states_):

        # Terminate when horizon is reached
        if count == 16:
            return global_cost, global_policy 
        cost = np.array([1,1,1,1])

        # Terminate early when goal is reached
        if np.allclose(new_state, start):
            print("reach the goal!")
            return global_cost, policy if global_policy is not None else global_policy
        
        # Set current parent state as goal
        goal = new_state
        # Get adjacent states
        new_states = goal - controls

        # Penalize the new state that go back to the last state
        if len(policy) > 0:
            goback_ind = np.where((controls==-policy[i]).all(axis=1))
            cost[goback_ind] += 1000

        # check out of bounds states
        mask = (new_states > 3) | (new_states < 0)

        # set cost of start state to 0
        if np.where((new_states==start).all(axis=1)):
            cost[np.where((new_states==start).all(axis=1))] = 0

        idx = np.where(mask == True)[0]
        # Add large cost to invalid states
        cost[idx] += 1000
        min_cost = np.min(cost)
        low_cost_states = np.where(cost == min_cost)
        new_states = new_states[low_cost_states]

        if len(policy) == 0:
            for ind in low_cost_states[0]:
                global_cost.append(cost[ind])
                policy.append(controls[ind])
        else:
            for k, ind in enumerate(low_cost_states[0]):
                global_cost[i] += cost[ind]
                global_policy.append(np.concatenate([policy[i], controls[ind]]))
    return DP(new_states, policy, count+1)



global_policy = []
global_cost = []
count = 0
costs, policy = DP([goal])
print("Cost: ", costs)
print("Policy: ", policy)