import sys
import os
from random import random, randint

prefix = 'inputs/'

prog 	= 'src/client.py'
IP		= '127.0.0.10'
port	= '5000'
# Wtx	= '5'
# Tout	= '5'
# Perror= '0.5'

if len(sys.argv) == 3:
	IP   = sys.argv[1]
	port = sys.argv[2]

for arq in os.listdir(prefix):
	if randint(1,2) > 1:
		arquivo = prefix+arq
		Wtx		= str(randint(1,10))
		Tout	= str(randint(1,10))
		Perror	= str(random())

		comando = 'python '+prog+' '+arquivo+' '+IP+':'+port+' '+Wtx+' '+Tout+' '+Perror
		print('$', comando)
		os.system(comando)
