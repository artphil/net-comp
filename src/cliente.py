# Universidade Federal de Minas Gerais
# Arthur Phillip D. Silva & Gabriel Almeida de Jesus
# Cliente UDP

import socket
import sys
import string
import crypt
from struct import pack
from time import time

# Recebe e separa os Parametros Host e Port
HostPort = sys.argv[2]
P_Host, P_Port = HostPort.split(':')

HOST = P_Host		# Endereco IP do Servidor
PORT = int(P_Port)	# Porta que o Servidor esta

# Recebendo parametros de Entrada
arquivo = sys.argv[1]
tamJanela = int(sys.argv[3])
temporiz = int(sys.argv[4])
ProbErro = float(sys.argv[5])

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

# Tratamento da entrada
msg_id = 0

arq = open(arquivo, 'r')
linha = arq.readline()
tempo = time()
while linha:
	msg = linha[:-1]
	segundos = int(tempo)
	nanoseg = int((tempo-segundos)*1000000000)
	tam = len(linha)

	mhash = crypt.crypt(str(msg_id)+str(segundos)+str(nanoseg)+str(tam)+msg, crypt.METHOD_MD5)
	print (mhash)

	udp.sendto(pack('L', msg_id), dest)
	udp.sendto(pack('L', segundos), dest)
	udp.sendto(pack('I', nanoseg), dest)
	udp.sendto(pack('H', tam), dest)
	udp.sendto(msg.encode('latin1'), dest)
	udp.sendto(mhash.encode('latin1'), dest)

	linha = arq.readline()
	tempo = time()
	msg_id += 1

arq.close()
udp.close()
