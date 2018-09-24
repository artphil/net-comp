import sys
import os
from random import random, randint
from time import time

prefix = 'inputs/'

prog 	= 'src_test/client.py'
IP		= '127.0.0.10'
port	= '5000'
# Wtx	= '5'
# Tout	= '5'
# Perror= '0.5'

if len(sys.argv) == 3:
	IP   = sys.argv[1]
	port = sys.argv[2]

arq_log = 'logs/log_client_s05.csv'

log = open(arq_log, 'w')
log.write('Time, Perror, Wtx, Tout, ')
for i in range(20):
	log.write('msg ,tent., erro e, erro r, tout, ')
log.write('erro e total, reenvios, Tout total;\n')
log.close()

tempo = time()

'''
for arq in os.listdir(prefix):
	if randint(1,2) > 1:
		arquivo = prefix+arq
		Wtx		= str(randint(1,10))
		Tout	= str(randint(1,10))
		Perror	= str(random())

		comando = 'python '+prog+' '+arquivo+' '+IP+':'+port+' '+Wtx+' '+Tout+' '+Perror
		print('$', comando)
		os.system(comando)
'''
for e in range(0,100,10):
	for j in range(1,11):
		for t in range(1,6):

			arquivo = prefix+'teste.txt'
			t_inicio = int(time()-tempo)
			Perror	= str(e/100.0)
			Wtx		= str(j)
			Tout	= str(t)

			comando = 'python '+prog+' '+arquivo+' '+IP+':'+port+' '+Wtx+' '+Tout+' '+Perror+' '

			log = open(arq_log, 'a')
			# log.write(comando+'\n')
			log.write(str(t_inicio)+', '+str(Perror)+', '+str(Wtx)+', '+str(Tout)+', ')
			log.close()

			print('$', comando)
			os.system(comando+arq_log)


t_inicio = int(time()-tempo)
log = open(arq_log, 'a')
# log.write(comando+'\n')
log.write(str(t_inicio)+';\n ')
log.close()
