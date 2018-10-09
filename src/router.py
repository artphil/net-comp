'''
Universidade Federal de Minas Gerais
Trabalho pratico da disciplina Rede de Computadores da UFMG
Protocolo de Roteamento por Vetor de Distância
DCCRIP
Arthur Phillip D. Silva & Gabriel Almeida de Jesus
'''

# Bibliotecas
import socket
import sys
import json
import threading
from time import time
# from struct import pack, unpack, calcsize
'''
Chamada do programa

python router.py <ADDR> <PERIOD> [STARTUP]

ADDR	: endereço IP qual o roteador deve se associar
PERIOD	: periodo entre envio de mensagens de update
STARTUP	: arquivos utilizados para montar a topologia inicial dos roteadores
'''

'''					 Classes  				'''
class dest_gerenc:
	list = {}

	def __init__(self):
		self.d_lock = threading.Lock()

	# Adiciona ou atualista um destino na lista
	def addr_add(self, destino, custo, vizinho):
		d_lock.acquire()

		if destino in self.list:
			if destino == vizinho:
				if self.list[destino]['custo'] > custo:
					self.list[destino]['custo'] = custo
					self.list[destino]['vizinho'] = vizinho
			else:
				if self.list[destino]['custo'] > custo+self.list[vizinho]['custo']:
					self.list[destino]['custo'] = custo+self.list[vizinho]['custo']
					self.list[destino]['vizinho'] = vizinho
		else:
			self.list[destino]['vizinho'] = vizinho
			if destino == vizinho:
				self.list[destino]['custo'] = custo
			else:
				self.list[destino]['custo'] = custo+self.list[vizinho]['custo']

		d_lock.release()

	def addr_del(self, destino):
		d_lock.acquire()

		if destino in self.list:
			del self.list[destino]

		d_lock.release()

'''					 Funcoes  				'''
def le_comando():
	global ligado
	while ligado:
		cmd = input().split(" ")
		if cmd[0] == 'add' and len(cmd)>2:
			print('add nao implantado')
		elif cmd[0] == 'del' and len(cmd)>1:
			print('del nao implantado')
		elif cmd[0] == 'trace' and len(cmd)>2:
			print('trace nao implantado')
		elif cmd[0] == 'quit':
			ligado = False
		else:
			print('comando invavido')

def envia_custos():
	global tempo, tout, ligado
	while ligado:
		if tempo+tout < time():
			tempo = time()
			pass

def recebe():
	global ligado
	while ligado:
		pacote, addr = udp.recvfrom(1024)

'''					Programa				'''
# Recebe e separa os Parametros Host e Port
HOST = sys.argv[1]			# Endereco IP do roteador
PORT = 55151				# Porto do roteador

# Criando socket de comunicacao UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
orig = (HOST, PORT)
udp.bind(orig)

# Variaveis de controle
tempo = time()
tout = int(sys.argv[2])
destinos = dest_gerenc()
ligado = True

if len(sys.argv) > 3:
	for arq in sys.argv[3:]:
		with open(arq, "r") as arq_start:
			for dest in arq_start.readline():
				cmd = dest[:-1].split(" ")
				if cmd[0] == 'add':
					destinos.addr_add(cmd[1], cmd[2], cmd[1])
				if cmd[0] == 'del':
					destinos.addr_del(cmd[1])

# Execucao do programa
comando = threading.Thread(target=le_comando)
# envio = threading.Thread(target=envia_custos)
# receb = threading.Thread(target=recebe)

# Inicia as threads
comando.start()
# envio.start()
# receb.start()

# Espera retorno
comando.join()
# envio.join()
# receb.join()
