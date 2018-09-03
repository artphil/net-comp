# Universidade Federal de Minas Gerais
# Arthur Phillip D. Silva & Gabriel Almeida de Jesus
# Servidor UDP

import socket
import sys
import crypt
from struct import unpack
from time import time
from hmac import compare_digest as compare_hash

def dprint (d):
	print('--------------Data----------------')
	for k, v in d.items():
		print (k)
		for kk, vv in v.items():
			print ('	', kk, '	:', vv)
		print()
	print('----------------------------------')


HOST = ''					# Endereco IP do Servidor
PORT = int(sys.argv[2])		# Porta que o Servidor esta

# Recebendo parametros de Entrada
arquivo = sys.argv[1]
tamJanela = int(sys.argv[3])
probErro = float(sys.argv[4])

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
orig = (HOST, PORT)
udp.bind(orig)

# Tratamento log
arq_log = open(arquivo, 'w')


# Tratamento de conversas
variaveis = ['id', 'seg', 'ns', 'sz', 'msg', 'md5']
v_pack = ['L', 'L', 'I', 'H']
cliente_list = {}

while True:
	msg, cliente = udp.recvfrom(1024)
	if cliente not in cliente_list:
		cliente_list[cliente] = {}
		ordem = cliente_list[cliente]['ordem'] = 0
		cliente_list[cliente]['tempo'] = time()
		cliente_list[cliente][variaveis[ordem]] = unpack('L', msg)[0]
	else:
		cliente_list[cliente]['tempo'] = time()
		ordem = cliente_list[cliente]['ordem']
		if ordem < 4:
			cliente_list[cliente][variaveis[ordem]] = unpack(v_pack[ordem], msg)[0]
		else:
			cliente_list[cliente][variaveis[ordem]] = msg.decode('latin1')

	cliente_list[cliente]['ordem'] += 1

	if cliente_list[cliente]['ordem'] > 5:
		cliente_list[cliente]['ordem'] = 0
		data = ''
		for value in variaveis[:-1]:
			data += str(cliente_list[cliente][value])
		chash = compare_hash(crypt.crypt(data, cliente_list[cliente]['md5']), cliente_list[cliente]['md5'])

		print ('chash= ', chash)
		if chash:
			arq_log.write(cliente_list[cliente]['msg']+'\n')

	dprint(cliente_list)

udp.close()
