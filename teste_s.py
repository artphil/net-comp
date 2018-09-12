import sys
import os
from random import random, randint
import time

prefix = 'logs/'

prog 	= 'src/servero.py'
port	= '5000'
# Wrx	= '5'
# Perror= '0.5'

if len(sys.argv) == 2:
	port = sys.argv[1]

print(strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
arquivo = prefix+'a.out'
#str()
Wrx		= str(randint(1,10))
Perror	= str(random())

comando = 'python '+prog+' '+arquivo+' '+port+' '+Wrx+' '+Perror
print('$', comando)
os.system(comando)
