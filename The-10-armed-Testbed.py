import matplotlib.pyplot as plt
import numpy as np


class bandit:
	def __init__(self, k, eps, step, mu):
		self.k = k
		self.eps = eps
		self.step =step
		self.n = 0
		self.k_n = np.zeros(k)
		self.mean_reward = 0
		self.mean_step_reward = np.zeros(step)
		self.k_value = np.zeros(k)
		self.mu = mu

	def run(self):
		for t in range(step):
			token = np.random.rand()
			a = np.argmax(self.k_value)
			if token < self.eps:
				a = np.random.choice(self.k)
  			reward = np.random.normal(self.mu[a],1)
  			self.n+=1
  			self.k_n[a]+=1
  			self.mean_reward = self.mean_reward + (reward - self.mean_reward)/self.n
  			self.k_value[a] = self.k_value[a] + (reward - self.k_value[a])/self.k_n[a]
  			self.mean_step_reward[t] = self.mean_reward

	def decay_run(self):
		for t in range(step):
			token = np.random.rand()
			a = np.argmax(self.k_value + 2* np.sqrt(np.log(t)/self.k_n))
  			reward = np.random.normal(self.mu[a],1)
  			self.n+=1
  			self.k_n[a]+=1
  			self.mean_reward = self.mean_reward + (reward - self.mean_reward)/self.n
  			self.k_value[a] = self.k_value[a] + (reward - self.k_value[a])/self.k_n[a]
  			self.mean_step_reward[t] = self.mean_reward

	def avg_run(self, episode):
		tmp = np.zeros(self.step)
		for i in range(episode):
			self.reset()
			self.run()
			tmp = tmp + (self.mean_step_reward - tmp)/(i+1)
		return tmp

	def decay_avg_run(self, episode):
		tmp = np.zeros(self.step)
		for i in range(episode):
			self.reset()
			self.decay_run()
			tmp = tmp + (self.mean_step_reward - tmp)/(i+1)
		return tmp

	def reset(self):
		self.n = 0
		self.k_n = np.zeros(self.k)
		self.mean_reward = 0
		self.mean_step_reward = np.zeros(step)
		self.k_value = np.zeros(self.k)

            

k = 10
step = 1000
episode = 2000
q = np.random.normal(0, 1, k)
b = bandit(k, 0.1, step, q)



plt.figure(figsize=(7,5))
plt.plot(b.avg_run(episode), label="$\epsilon=0.1$", color = "green")
plt.plot(b.decay_avg_run(episode), label="$\epsilon=decay$", color = "red")
plt.legend(bbox_to_anchor=(0.7, 0.5))
plt.xlabel("Iterations")
plt.ylabel("Average Reward")
plt.title("Average $\epsilon-greedy$ Rewards after " + str(episode) 
    + " Episodes")
print(q)
plt.show()
