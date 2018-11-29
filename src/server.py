'''
Universidade Federal de Minas Gerais
Trabalho pratico da disciplina Rede de Computadores da UFMG
Protocolo HTTP e servico REST
Arthur Phillip D. Silva & Gabriel Almeida de Jesus
Servidor
'''

import json
import socket
import sys

MAX_TAM = 1024

HOST = '' # Endereco de IP do Servidor
PORT = int(sys.argv[1]) # Porta que o Servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)

# Abertura passiva de Conexão
tcp.bind(orig)
tcp.listen(1)
print('Servidor Escutando')

def responde(con, cliente):
	print('Conectado com ', cliente)
	request = con.recv(MAX_TAM).decode('latin1')

	print('Requisicao = ', request)

while True:
	# Aceitando Conexões
	con, cliente = tcp.accept()
	con.settimeout(15)
	responde(con, cliente)

# Fecha Conexão
tcp.close()
