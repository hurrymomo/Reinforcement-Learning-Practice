import matplotlib.pyplot as plt
import numpy as np
import copy
size = 4
grid=[[0 for i in range(size)] for j in range(size)]
grid[0][0]=1
grid[size-1][size-1]=1
eps   = 0.001
#V = np.array(copy.deepcopy(grid))
#V = V.astype(float)
V=[[0 for i in range(size)] for j in range(size)]
def backup(i, j):
	global V,size
	return -1 + V[i][j]

while True:
	delta = 0
	for i in range(size):
		for j in range(size):
			if( i == 0 and j ==0 ):
				continue
			if( i == size -1 and j == size -1):
				continue
			newV = sum([backup(max(i-1,0),j),backup(min(i+1,size-1),j),backup(i,max(j-1,0)),backup(i,min(j+1,size-1))])/4
			delta = max(delta, abs(newV - V[i][j]))
			V[i][j] = newV
	if(delta < eps):
		break;

for i in range(size):
	print(V[i])