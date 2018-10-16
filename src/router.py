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

Exemplos de pacotes enviados:
{
	"type": "data",
	"source": "127.0.1.2",
	"destination: "127.0.1.1",
	"payload": "{\"destination\": \"127.0.1.2\", \"type\": \"trace\", ...}"
}

{
	"type": "update",
	"source": "127.0.1.5",
	"destination": "127.0.1.1",
	"distances": {
		"127.0.1.4": 10,
		"127.0.1.5": 0,
		"127.0.1.2": 10,
		"127.0.1.3": 10
	}
}

{
	"type": "trace",
	"source": "127.0.1.1",
	"destination": "127.0.1.2",
	"hops": ["127.0.1.1", "127.0.1.5"]
}
'''

'''					 Classes  				'''

'''
Estruturas:
vizinhos = {
	<vizinho>:<custo>
	<vizinho>:<custo>
	...
}
destinos = {
	<destino>:{
		<vizinho>:<custo>
		<vizinho>:<custo>
		...
	}
	<destino>:{
		<vizinho>:<custo>
		...
	}
}
'''
# Gerenciador de vizinhos e destinos possiveis
class dest_gerenc:

	def __init__(self):
		self.destinos = {} # Lista de destinos possiveis
		self.vizinhos = {} # Lista de vizinhos

		# controle de concorrencia
		self.d_lock = threading.Lock()
		self.v_lock = threading.Lock()

	# Atualisa a tabela de vizinhos e destinos
	def viz_add(self, vizinho, custo):
		self.v_lock.acquire()

		self.vizinhos[vizinho] = int(custo)

		self.v_lock.release()

		self.dest_add(vizinho, custo, vizinho)

	# Remove vizinhos e os destinos relativos
	def viz_del(self, vizinho):
		self.v_lock.acquire()
		# verifica se vizinho existe e o remove
		if vizinho in self.vizinhos:
			del self.vizinhos[vizinho]
		else:
			print(vizinho+' não encontrado')

		self.v_lock.release()

		self.dest_del(vizinho)

	# Atualisa a tabela de destinos
	def dest_add(self, destino, custo, vizinho):
		self.d_lock.acquire()

		c = int(custo)
		# Atualisa destinos já existentes
		if destino in self.destinos:
			if destino == vizinho:
				self.destinos[destino][vizinho] = c
			else:
				self.destinos[destino][vizinho] = c+self.vizinhos[vizinho]

			self.destinos[destino] = sorted(self.destinos[destino],key = self.destinos[destino].get())

		# insere vizinhos novos
		else:
			self.destinos[destino] = {}
			if destino == vizinho:
				self.destinos[destino][vizinho] = c
			else:
				self.destinos[destino][vizinho] = c+self.vizinhos[vizinho]

		self.d_lock.release()

	def dest_del(self, destino): ## ERRADO
		self.d_lock.acquire()

		# Remove destinos da tabela
		if destino in self.destinos:
			del self.destinos[destino]

		# Procura rotas que usam o destino e remove esta opcao
		apagar = []
		for k,v in self.destinos:
			if destino in v:
				del v[destino]
				# Identifica destinos sem rota
				if len(v) == 0:
					apagar.append(k)
		# Remove destinos que nao sao mais alcancaveis
		for d in apagar:
			del self.destinos[d]

		self.d_lock.release()

	def dest_update(self, dic, vizinho):
		self.d_lock.acquire()
		apagar = []
		# Confere de todos os destinos
		for d,v in self.destinos.items():
			# Caminhos que nao sao mais validos
			if d is not in dic:
				# E estao registados na estrutura
				if vizinho is in v:
					# E os remove
					del v[vizinho]
					# Identifica destinos sem rota
					if len(v) == 0:
						apagar.append(d)
		# Remove destinos que nao sao mais alcancaveis
		for d in apagar:
			del self.destinos[d]
		self.d_lock.release()

		# Adiciona ou atualiza caminhos validos
		for d,c in dic:
			self.dest_add(d, c, vizinho)


	# Lista de destinos com custos de vizinhos por onde passar
	def to_print(self):
		p = []
		self.d_lock.acquire()
		for k,v in self.destinos.items():
			viz = list(v)[0]
			# print(k,viz,v)
			p.append([k,v[viz],viz])
		self.d_lock.release()

		return p

	def dest_list(self):
		d = {}
		self.d_lock.acquire()
		for k,v in self.destinos.items():
			viz = list(v)[0]
			d[k] = str(v[viz])
		self.d_lock.release()

		return d



'''					 Funcoes  				'''
def le_comando():
	global ligado
	while ligado:
		cmd = input().split(" ")

		if cmd[0] == 'add' and len(cmd)>2:
			# print('add nao implantado')
			destinos.viz_add(cmd[1], cmd[2])

		elif cmd[0] == 'del' and len(cmd)>1:
			# print('del nao implantado')
			destinos.viz_del(cmd[1])

		elif cmd[0] == 'trace' and len(cmd)>2:
			print('trace nao implantado')

		elif cmd[0] == 'print':
			for valor in destinos.to_print():
			# for valor in destinos.dest_list().items():
				print(valor)

		elif cmd[0] == 'quit':
			ligado = False

		else:
			print('comando invavido')

def envia_custos():
	global tempo, tout, ligado, HOST, PORT
	while ligado:
		if tempo+tout < time():
			tempo = time()
			dest = destinos.dest_list()
			pac = {
			"type": "update",
			"source": HOST,
			"distances": dest
			}
			for d in dest:
				if d != HOST:
					pac ["destination"] = d
					pacote = json.dumps(pac)
					# print(pacote)
					udp.sendto(pacote.encode('latin1'), (d, PORT))


def recebe():
	global ligado
	while ligado:
		pacote, addr = udp.recvfrom(1048576)
		pac = json.loads(pacote.decode('latin1'))
		# print ("recived: ",addr[0])
		v = addr[0]
		if pac['type'] == 'update':
			destinos.dest_update(pac['distances'], v)

		elif pac['type'] == 'trace':
			pass

		elif pac['type'] == 'data':
			pass


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

destinos.viz_add(HOST, '0')

if len(sys.argv) > 3:
	for arq in sys.argv[3:]:
		with open(arq, "r") as arq_start:
			for dest in arq_start.readline():
				cmd = dest[:-1].split(" ")
				if cmd[0] == 'add':
					destinos.viz_add(cmd[1], cmd[2])
				if cmd[0] == 'del':
					destinos.viz_del(cmd[1])

# Execucao do programa
comando = threading.Thread(target=le_comando)
envio = threading.Thread(target=envia_custos)
receb = threading.Thread(target=recebe, daemon=True)

# Inicia as threads
comando.start()
envio.start()
receb.start()

# Espera retorno
comando.join()
envio.join()
# receb.join()
