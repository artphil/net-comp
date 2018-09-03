# Universidade Federal de Minas Gerais
# Arthur Phillip D. Silva & Gabriel Almeida de Jesus
# Cliente UDP

import socket
import sys
import string

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

print ('Para sair use CTRL+X\n')
msg = input()
while msg != '\x18':
	udp.sendto(msg.encode('latin1'), dest)
	msg = input()

udp.close()
