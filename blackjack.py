import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson


V = np.full((2,22,11),0.0)
N = np.full((2,22,11),0)
player = []
dealer  = []

def draw():
	return np.random.randint(1,11)
def isBust(deck):
	return sum(deck)>21
def isNatural(deck):
	return deck.count(1) and deck.count(10)
episode = 500000
record = []


for t in range(episode):
	epi = []
	player=[draw(), draw()]
	dealer=[draw(), draw()]
#	print("player", player)
#	print("dealer", dealer)
	usable = player.count(1)>0
#	print("natural ?")
	if isNatural(player) and isNatural(dealer):
#		print("natural draw")
		epi += [[dealer[0], 21, usable]]
		record+=[[epi,0]]
		continue
	elif isNatural(player):
#		print("natural player win")
		epi += [[dealer[0], 21, usable]]
		record+=[[epi,1]]
		continue
	elif isNatural(dealer):
#		print("natural dealer win")
		tot = sum(player)
		if usable:
			tot+=10
		epi += [[dealer[0], tot, usable]]
		record+=[[epi,-1]]
		continue

	#player
#	print("No natural")
#	print("Player Turn")
	tot = sum(player)
	usable = player.count(1)>0 
	if usable:
		tot+=10
	epi += [[dealer[0], tot, usable]]
#	print("tot: ", tot)
	while tot < 20 :
		card = draw()
#		print("draw card: ",card)
		tot+=card
		if usable and tot > 21:
			usable = False
			tot-=10
		elif not usable and tot+10 < 21:
			usable = True
			tot+=10
		epi += [[dealer[0], tot, usable]]
#	print("Player Turn end with: ", tot)
	if tot > 21:
#		print("Player bust ", tot)
		record +=[[epi, -1]]
		continue

#	print("Dealer Turn")
	dtot = sum(dealer)
	dusable = dealer.count(1)>0
	if dusable:
		dtot+=10
#	print("dtot: ", dtot)
	while dtot < 17 :
		card = draw()
#		print("draw card: ",card)
		dtot+=card
		if dusable and dtot > 21:
			dusable = False
			dtot-=10
		elif not dusable and dtot+10 < 21:
			dusable = True
			dtot+=10
#	print("Dealer Turn end with: ", dtot)
	if dtot > 21:
#		print("Dealer bust ", dtot)
		record +=[[epi, 1]]	
		continue
	if(dtot == tot):
#		print("Draw, player: ", tot, " vs dealer: ", dtot)
		record +=[[epi, 0]]	
	elif tot > dtot:
#		print("Player win, player: ", tot, " vs dealer: ", dtot)
		record +=[[epi, 1]]
	else:
#		print("Dealer win, player: ", tot, " vs dealer: ", dtot)
		record +=[[epi, -1]]


for data, reward in record:
	for step in data:
		if step[1]>21:
			continue
		a = step[2]
		if a:
			a = 1
		else:
			a = 0
		b = step[1]
		c = step[0]
		N[a][b][c]+=1
		n = N[a][b][c]
		v = V[a][b][c]
		V[a][b][c]= v+ (reward - v)/n	


fig = plt.figure(figsize=(6, 3.2))

ax = fig.add_subplot(111)
ax.set_title('colorMap')
plt.imshow(V[0])
ax.set_aspect('equal')

cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
cax.get_xaxis().set_visible(False)
cax.get_yaxis().set_visible(False)
cax.patch.set_alpha(0)
cax.set_frame_on(False)
plt.colorbar(orientation='vertical')
plt.show()





