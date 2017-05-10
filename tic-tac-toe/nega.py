import itertools
import random

"""
Lo = [-1, 4, -3, -2, 0 ,2, 3, -4, 1]
b = dict(zip(Lo, [0]*9))
b = {-4: 1, -3: 0, -2: -1, -1: 0, 0: 1, 1: 0, 2: 0, 3: -1, 4: 0}
"""

def c(b):
	
	for s in [1, -1]:
		l = [k for k, v in b.items() if v == s]
		l = list(itertools.combinations(l, 3))
		if len(l) > 0:
			for i in l:
				if sum(i) == 0: 
					return [-1, 1][s == 1] 
	return 0


def negamax(b, aa, bb, t, Lo):

	w = c(b)
	if w != 0:
		return t * w
	if 0 not in b.values():       
		return 0  
	r = -2	
	for m in Lo:
		if b[m] == 0:
			b[m] = t		
			v = -negamax(b, -bb, -aa, -t, Lo)
			b[m] = 0
			r = max([r, v])
			aa = max([aa, v])
			if aa >= bb:
				break
	return r


def best_move(b,Lo):

	lk = []
	lv = []
	for m in Lo:
			if b[m] == 0:
				b[m] = 1          
				v = -negamax(b, -2, 2, -1, Lo)
				b[m] = 0
				lk.append(m)
				lv.append(v)
	m = max(lv)		
	l = dict(zip(lk, lv))	
	return random.choice([k for k, v in l.items() if v == m])
