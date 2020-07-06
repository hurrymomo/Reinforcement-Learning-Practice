import matplotlib.pyplot as plt
import numpy as np
a=[]
class randWalk:
	def __init__(self, state_num, start, alpha,gamma, episode):
		self.V = [0.5]*state_num
		self.alpha= alpha
		self.start = start
		self.episode = episode
		self.gamma = gamma

	def MCrun(self):
		for t in range(self.episode):
			cur = self.start
			visited = [cur]
			reward = 0
			while(True):
				if np.random.rand() < 0.5:
					cur-=1
				else:
					cur+=1
				if cur == 0:
					break
				if cur==len(self.V)-1:
					reward = 1
					break
				visited.append(cur)
			for state in visited:
				old_state = self.V[state]
				self.V[state] = old_state+ self.alpha*(reward-old_state)
	def MCexp(self, run):
		V = np.array([0]*state_num)
		for t in range(run):
			self.MCrun()
			t+=1
			V = V + (np.array(self.V)-V)/t
		return V

	def TDrun(self):
		for t in range(self.episode):
			cur = self.start
			reward = 0
			while(True):
				old_state = cur
				if np.random.rand() < 0.5:
					cur-=1
				else:
					cur+=1
				if(cur == len(self.V)-1):
					reward = 1
				self.V[old_state] = self.V[old_state]+ self.alpha*(reward+self.gamma*self.V[cur]-self.V[old_state])
				if cur == 0 or cur==len(self.V)-1:
					break
	def TDexp(self, run):
		V = np.array([0]*state_num)
		for t in range(run):
			self.TDrun()
			t+=1
			V = V + (np.array(self.V)-V)/t
		return V



#w = randWalk(7,3,0.1)
state_num = 7
start = 3
alpha = 0.1
gamma = 1
episode = 100
run  = 100

v0 = randWalk(state_num,start,alpha,gamma,episode).TDexp(run)
v1 = randWalk(state_num,start,alpha,gamma,1).MCexp(10)
v2 = randWalk(state_num,start,alpha,gamma,10).MCexp(100)
v3 = randWalk(state_num,start,alpha,gamma,100).MCexp(100)
plt.plot(v1)

plt.show()
print(v0)

