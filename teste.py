import sys
import os
from random import random

prog 	= 'src/client.py'
arquivo = 'inputs/teste.txt'
IP		= '127.0.0.10'
port	= '5000'
Wtx		= '5'
Tout	= '5'
Perror	= '0.5'
# Perror	: 'str(random())'

comando = 'python '+prog+' '+arquivo+' '+IP+':'+port+' '+Wtx+' '+Tout+' '+Perror
os.system(comando)
