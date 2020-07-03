import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson

loc1 = 20
loc2 = 20
eps = 0.0000001
mu_request= [3,4]
mu_dropoff= [3,2]
R1 = [0.0 for i in range(26)]
R2 = [0.0 for i in range(26)]
#P1 = [[0.0]*21]*26 <- dont try this 
#P2 = [[0.0]*21]*26
P1 = [[0.0 for i in range(21)] for j in range(26)]
P2 = [[0.0 for i in range(21)] for j in range(26)]
V  = [[0.0 for i in range(21)] for j in range(21)]
Policy = [[0 for i in range(21)] for j in range(21)]
gamma = 0.9



def load_P_R(P,R,mu_request, mu_dropoff, eps):
	request = 0
	while True:
		request_prob =  poisson.pmf(request,mu_request)
		for n in range(26): # given n car in the morining, the expeceted reward R[n]
			R[n] += request_prob * 10 * min(n, request)
		dropoff = 0
		while True:
			dropoff_prob = poisson.pmf(dropoff,mu_dropoff)
			for n in range(26):# given n car in the morning
				satisfied_request = min(request, n)
				new_n = max(0, min(20, n+dropoff-satisfied_request))
				# probability having n car in the morning and new_n in the night
				P[n][new_n] += (request_prob*dropoff_prob)
			if dropoff_prob < eps:
				break
			dropoff+=1
		if request_prob < eps:
			break
		request+=1
load_P_R(P1,R1,mu_request[0],mu_dropoff[0],eps)
load_P_R(P2,R2,mu_request[1],mu_dropoff[1],eps)

def backup(l1, l2, a):
	global R1,R2,P1,P2,gamma,V
	a = max(-l2, min(a, l1))
	a = max(-5, min(5, a))
	rst = 0
	morning_n1 = l1 - a
	morning_n2 = l2 + a
	for n1 in range(21):
		for n2 in range(21):
			rst+= P1[morning_n1][n1]*P2[morning_n2][n2]*(R1[morning_n1]+R2[morning_n2] + gamma*V[n1][n2])
	return rst - 2*abs(a)

def policy_eval():
	global V,Policy,eps
	while True:
		delta = 0
		for i in range(21):
			for j in range(21):
				old = V[i][j]
				a = Policy[i][j]
				V[i][j] = backup(i, j, a)
				delta = max(delta, abs(V[i][j] - old))
		if delta < eps:
			break

def find_policy(n1, n2):
	global eps
	best_value = -1
	best_action = 0
	for a in range(max(-5, -n2), min(5, n1)+1):
		tmp = backup(n1,n2,a)
		if tmp > best_value+eps:
			best_value = tmp
			best_action = a
	return best_action

def policy_improv():
	global Policy
	improve = False
	for n1 in range(21):
		for n2 in range(21):
			b = Policy[n1][n2]
			Policy[n1][n2] = find_policy(n1,n2)
			if b != Policy[n1][n2]:
				improve = True
	return improve
'''
while True:
	print("eval")
	policy_eval()
	print("improve")
	if(policy_improv() == False):
		break
	for i in range(20,-1,-1):
		print(Policy[i])
'''
while True:
	print("eval")
	delta = 0
	for n1 in range(21):
		for n2 in range(21):
			tmp = V[n1][n2]
			V[n1][n2] = backup(n1,n2,find_policy(n1,n2))
			delta = max(delta, abs(tmp - V[n1][n2]))
	if(delta < eps):
		break
	print(delta)
	
print("improve")
for n1 in range(21):
	for n2 in range(21):
		Policy[n1][n2]=find_policy(n1,n2)
for i in range(20,-1,-1):
	print(Policy[i])