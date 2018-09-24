import sys
import os
from random import random, randint
from time import gmtime, strftime

prefix = 'logs/'

prog 	= 'src/server.py'
port	= '5000'
# Wrx	= '5'
# Perror= '0.5'

if len(sys.argv) == 2:
	port = sys.argv[1]

arq = strftime("log_%Y%b%d_%Hh%Mm%Ss.dat", gmtime())
arquivo = prefix+arq
Wrx		= '5' #str(randint(1,10))
Perror	= '0.5' #str(random())

comando = 'python '+prog+' '+arquivo+' '+port+' '+Wrx+' '+Perror
print('$', comando)
os.system(comando)
