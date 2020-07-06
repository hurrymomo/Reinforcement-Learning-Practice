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

# Sarsa On policy
world = np.full((7,10,4),0.0)
wind  = np.array([0,0,0,1,1,1,2,2,1,0])
start = [3,0]
goal  = [3,7]
eps   = 0.01
alpha = 0.5
gamma = 1
delta = 0.0001
step = 1
def action_perform(cur, action):
	global wind, world
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
	state[0]-= wind[state[1]]
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

def each_epis():
	global start, alpha, gamma, eps, world,step
	cur_state = start
	cur_action = eps_greedy_selection(cur_state, 1.0/step)
	inp = ""
	while(cur_state!=goal):
		'''
		if not inp.isdigit():
			inp = raw_input()
		elif(t == int(inp)):
			inp = raw_input()
		'''
		step+=1
		reward = -1
		next_state = action_perform(cur_state, cur_action)
		next_action = eps_greedy_selection(next_state, 1.0/step)
		if(next_state == goal):
			reward = 1
		#print("cur_state: ",cur_state, " cur_action: ",cur_action, " next_state: ",next_state, " next_action: ",next_action, "t: ",t,1.0/t)
		#print("before update ",cur_state,cur_action,world[cur_state[0]][cur_state[1]])
		old_cur_Q = world[cur_state[0]][cur_state[1]][cur_action]
		old_next_Q = world[next_state[0]][next_state[1]][next_action]
		world[cur_state[0]][cur_state[1]][cur_action] = old_cur_Q + alpha*(reward + gamma*old_next_Q - old_cur_Q)
		#print("after update ",cur_state,cur_action,world[cur_state[0]][cur_state[1]])
		cur_state = next_state
		cur_action = next_action


def best_world():
	global world
	best = np.full((7,10),0)
	for i in range(len(world)):
		for j in range(len(world[i])):
			best[i][j] = (np.argmax(world[i][j]))
	return best

t = 0
time=[]
while(1):
	t+=1
	old =np.array(world)
	each_epis()
	time.append(step)
	new =np.array(world)
	diff = np.amax(abs(old-new))
	if diff < delta:
		break
	print(diff)
print("total epis",t)
#where you go at each position
bw = best_world()
print(bw)
for i in range(len(bw)):
	for j in range(len(bw[i])):
		print(action_perform([i,j],bw[i][j])),
	print("")

#plt.plot(time)
#plt.show()