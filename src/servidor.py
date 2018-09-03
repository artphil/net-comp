# Universidade Federal de Minas Gerais
# Arthur Phillip D. Silva & Gabriel Almeida de Jesus
# Servidor UDP

import socket
import sys
from struct import unpack, calcsize

HOST = ''					# Endereco IP do Servidor
PORT = int(sys.argv[2])		# Porta que o Servidor esta

# Recebendo parametros de Entrada
arquivo = sys.argv[1]
tamJanela = int(sys.argv[3])
probErro = float(sys.argv[4])

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
orig = (HOST, PORT)
udp.bind(orig)

# Tratamento de conversas
variaveis = ['id', 'seg', 'ns', 'sz', 'msg', 'md5']
cliente_list = {}

while True:
	msg, cliente = udp.recvfrom(1024)
	print (cliente, msg)

udp.close()
