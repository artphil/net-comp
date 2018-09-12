import sys
import os
from random import randint

prefix 	= 'inputs/'
sufix 	= '.txt'

alfa = 'abcdefghijklmnopqrstuvwxyz '
ta = len(alfa)-1

for x in range(100):
	a = open(prefix+str(x)+sufix, 'w')
	nl = randint(5,1000)
	for l in range(nl):
		nc = randint(1,200)
		for c in range(nc):
			a.write(alfa[randint(0,ta)])
		a.write('('+str(x)+')\n')
	a.close()
