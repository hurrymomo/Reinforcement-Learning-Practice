import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

# world 
# 0 1 2
# 1
# 2

#action
# 1
#0 2
# 3

world = np.full((4,12,4),0.0)
start = [3,0]
goal  = [3,11]
eps   = 0.1
alpha = 0.5
gamma = 1
delta = 0.0000001
step = 1

def action_perform(cur, action):
	global world
	state = list(cur)
	if(action == 0):
		state[1]-=1
	elif(action == 1):
		state[0]-=1
	elif(action == 2):
		state[1]+=1
	else:
		state[0]+=1
	state[1] = max(min(state[1],len(world[0])-1), 0)	
	state[0] = max(min(state[0],len(world)-1), 0)
	return state

def eps_greedy_selection(cur_state, eps):
	global world
	token = np.random.rand()
	action = np.argmax(world[cur_state[0]][cur_state[1]])
	#print(world[cur_state[0]][cur_state[1]])
	if(token < eps):
		action = np.random.choice([0,1,2,3])
	return action

def each_episode():
	global start,step,world,alpha,gamma,eps,goal
	cur_state = start
	cur_action = eps_greedy_selection(cur_state, eps)
	inp = ""
	tot_reward = 0
	while(cur_state != goal):
		step+=1
		'''
		if not inp.isdigit():
			inp = raw_input()
		elif(step == int(inp)):
			inp = raw_input()
		'''
		next_state = action_perform(cur_state, cur_action)
		reward = -1
		if next_state[0] == 3 and next_state[1] in range(1,11):
			reward = -100
			next_state = start
		if cur_state == goal:
			reward = 0
		next_action = eps_greedy_selection(next_state, eps)

		#print("cur_state: ",cur_state, " cur_action: ",cur_action, " next_state: ",next_state, " next_action: ",next_action, "t: ",step,eps)
		#print("before update ",cur_state,cur_action,world[cur_state[0]][cur_state[1]])
		old_world = world[cur_state[0]][cur_state[1]][cur_action]
		next_world = world[next_state[0]][next_state[1]][next_action]
		world[cur_state[0]][cur_state[1]][cur_action] = old_world + alpha*(reward + gamma * next_world - old_world)
		#print("after update ",cur_state,cur_action,world[cur_state[0]][cur_state[1]])
		cur_state = next_state
		cur_action = next_action
		tot_reward+=reward
	return tot_reward
def best_world():
	global world
	best = np.full((4,12),0)
	for i in range(len(world)):
		for j in range(len(world[i])):
			best[i][j] = (np.argmax(world[i][j]))
	return best

time = []
run = 0
while(run < 5000):
	print("run",run)
	old = np.array(world)
	each_episode()
	time.append(step)
	new = np.array(world)
	run+=1
	diff = np.amax(abs(old-new))
	if diff < delta:
		break
	print(diff)
print(best_world())
#axes = plt.gca()
#axes.set_ylim([-50, 1])

plt.plot(time)
plt.show()