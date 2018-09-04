# Universidade Federal de Minas Gerais
# Arthur Phillip D. Silva & Gabriel Almeida de Jesus
# Servidor UDP

import socket
import sys
import crypt
from struct import unpack, calcsize
from time import time
from hmac import compare_digest as compare_hash

def dprint (d):
	print('--------------Data----------------')
	for k, v in d.items():
		print (k)
		print ('	tempo	:', v['tempo'])
		print ('	gravado	:', v['gravar'])
		for k1, v1 in v['janela'].items():
			print ('	id:', k1)
			for k2, v2 in v1.items():
				print ('		', k2, '	:', v2)
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
cliente_list = {}

while True:
	pacote, cliente = udp.recvfrom(1024)

	parte = pacote[:calcsize('L')]
	pacote = pacote[calcsize('L'):]
	msg_id = unpack('L', parte)[0]

	parte = pacote[:calcsize('L')]
	pacote = pacote[calcsize('L'):]
	seg = unpack('L', parte)[0]

	parte = pacote[:calcsize('I')]
	pacote = pacote[calcsize('I'):]
	nseg = unpack('I', parte)[0]

	parte = pacote[:calcsize('H')]
	pacote = pacote[calcsize('H'):]
	tam = unpack('H', parte)[0]

	parte = pacote[:tam]
	pacote = pacote[tam:]
	msg = parte.decode('latin1')

	mhash = pacote.decode('latin1')
	chash = crypt.crypt(str(msg_id)+str(seg)+str(nseg)+str(tam)+msg, mhash)

	if compare_hash(mhash, chash):
		if cliente not in cliente_list:
			cliente_list[cliente] = {}
			cliente_list[cliente]['janela'] = {}
			cliente_list[cliente]['gravar'] = 0

		cliente_list[cliente]['tempo'] = time()

		if msg_id not in cliente_list[cliente]['janela']:
			if len(cliente_list[cliente]['janela']) < tamJanela:
				if msg_id >= cliente_list[cliente]['gravar'] and msg_id < (cliente_list[cliente]['gravar']+tamJanela):
					cliente_list[cliente]['janela'][msg_id] = {}
					cliente_list[cliente]['janela'][msg_id]['seg'] = seg
					cliente_list[cliente]['janela'][msg_id]['nseg'] = nseg
					cliente_list[cliente]['janela'][msg_id]['msg'] = msg
					cliente_list[cliente]['janela'][msg_id]['mhash'] = mhash

	for k, v in cliente_list.items():
		if v['gravar'] in v['janela']:
			arq_log.write(v['janela'][v['gravar']]['msg']+'\n')
			del v['janela'][ v['gravar'] ]
			v['gravar'] += 1

	dprint(cliente_list)

udp.close()
