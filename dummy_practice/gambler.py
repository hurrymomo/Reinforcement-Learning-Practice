import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson

V = [0.0 for i in range(101)]
V[100]=1
P = [0.0 for i in range(100)]
ph = 0.4
eps = 0.0000001


def backup(i, a):
	global ph
	return ph* ( V[i+a]) + (1-ph)*(V[i-a])

def best_action(i):
	global eps
	best_value = -1
	best_action = 0
	for a in range(1, min(i, 100-i)+1):
		print(i,a)
		tmp = backup(i, a)
		if tmp > best_value + eps:
			best_value = tmp
			best_action = a
	return best_action

print("eval")
while True:
	delta = 0
	for i in range(1,100):
		old = V[i]
		V[i] = backup(i, best_action(i));
		delta = max(delta, abs(old - V[i]))
	if delta < eps:
		break;
	print(delta)
print("improve")
for i in range(1,100):
	P[i] = best_action(i)

plt.plot(P)
plt.show()
