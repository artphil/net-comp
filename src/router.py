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
import operator
from time import time

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
tempo = {
	<vizinho>:<ultimo_update>
	<vizinho>:<ultimo_update>
	<vizinho>:<ultimo_update>
	...
}
'''
# Gerenciador de vizinhos e destinos possiveis
class dest_gerenc:
	# Connstrutor da classe
	def __init__(self):
		self.destinos = {} # Lista de destinos possiveis
		self.vizinhos = {} # Lista de vizinhos
		self.tempo = {} # Lista de ultimo updates

		# controle de concorrencia
		self.d_lock = threading.Lock()
		self.v_lock = threading.Lock()

	# Atualisa a tabela de vizinhos e destinos
	def viz_add(self, vizinho, custo):
		self.tempo[vizinho] = time()

		self.v_lock.acquire()

		self.vizinhos[vizinho] = int(custo)

		self.v_lock.release()

		# Atualisa destinos
		self.dest_add(vizinho, '0', vizinho)

	# Remove vizinhos e os destinos relativos
	def viz_del(self, vizinho):
		self.v_lock.acquire()
		# verifica se vizinho existe e o remove
		if vizinho in self.vizinhos:
			del self.vizinhos[vizinho]
			del self.tempo[vizinho]
		# else:
			# print(vizinho+' não encontrado')

		self.v_lock.release()

		# remove destino
		self.dest_del(vizinho)

	# Atualisa a tabela de destinos
	def dest_add(self, destino, custo, vizinho):
		# Verifica se conhece rota para o destino
		if vizinho in self.vizinhos:
			self.d_lock.acquire()
			# print(self.destinos)

			c = int(custo)
			# Atualisa destinos já existentes
			if destino in self.destinos:
				self.destinos[destino][vizinho] = c+self.vizinhos[vizinho]

				# Ordena vizinhos para destino pelo custo
				self.destinos[destino] = dict(sorted(self.destinos[destino].items(), key=operator.itemgetter(1)))
				# print(self.destinos[destino])

			# insere vizinhos novos
			else:
				self.destinos[destino] = {}
				self.destinos[destino][vizinho] = c+self.vizinhos[vizinho]

			self.d_lock.release()


	def dest_del(self, destino):
		self.d_lock.acquire()

		# Remove destinos da tabela
		if destino in self.destinos:
			del self.destinos[destino]

		# Procura rotas que usam o destino e remove esta opcao
		apagar = []
		for k,v in self.destinos.items():
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
		self.tempo[vizinho] = time()
		# print (json.dumps(self.tempo, indent=4))
		self.d_lock.acquire()
		apagar = []
		# print(dic)
		# Confere de todos os destinos
		for d,v in self.destinos.items():
			# Caminhos que nao sao mais validos
			if d not in dic:
				# E estao registados na estrutura
				if vizinho in v:
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
		for d,c in dic.items():
			self.dest_add(d, c, vizinho)

	# identifica o melhor caminho para o destino
	def viz_to_dest(self,dest):
		global balanceamento
		if dest in self.destinos:
			if list(self.destinos[dest])[0] != list(self.destinos[dest])[balanceamento]:
				balanceamento = 1
				return list(self.destinos[dest])[0]
			else:
				balanceamento = balanceamento + 1
				return list(self.destinos[dest])[balanceamento-1]

	# Lista [destino, custo, vizinho]
	def to_print(self):
		if self.destinos:
			p = []
			self.d_lock.acquire()
			for k,v in self.destinos.items():
				viz = list(v)[0]
				# print(k,viz,v)
				p.append([k,v[viz],viz])
			self.d_lock.release()
		else:
			p = ['vazio']
		return p

	# Lista de vizinhos
	def viz_list(self):
		return list(self.vizinhos)

	# Lista de destinos e custos
	def dest_list(self, vizinho):
		if self.destinos:
			d = {}
			self.d_lock.acquire()
			for k,v in self.destinos.items():
				# Destinos que nao sao o vizinho e que nao vieram dele
				if vizinho != k and vizinho != list(v)[0]:
					viz = list(v)[0]
					d[k] = str(v[viz])

			self.d_lock.release()

			return d

	def list_timeout(self, tt):
		tout = []
		for v,t in self.tempo.items():
			if t+tt < time():
				tout.append(v)

		return tout


'''					 Funcoes  				'''
# Recebe e interpreta comandos do teclado
def le_comando():
	global ligado, HOST, PORT
	while ligado:
		cmd = input().split(" ")
		# Adiciona vizinho
		if cmd[0] == 'add' and len(cmd)>2:
			# print('add nao implantado')
			destinos.viz_add(cmd[1], cmd[2])
		# Remove vizinho
		elif cmd[0] == 'del' and len(cmd)>1:
			# print('del nao implantado')
			destinos.viz_del(cmd[1])
		# Efetua ping
		elif cmd[0] == 'trace' and len(cmd)>1:
			# print('trace nao implantado')
			dest = destinos.viz_to_dest(cmd[1])
			if dest:
				pac = {
					"type": "trace",
					"source": HOST,
					"destination": cmd[1],
					"hops": [HOST]
				}
				pacote = json.dumps(pac)
				# print(pacote)
				udp.sendto(pacote.encode('latin1'), (dest, PORT))
			# else:
				# print(cmd[1], 'nao pode ser alcancado')
		# imprime destinos conhecidos
		elif cmd[0] == 'print':
			for valor in destinos.to_print():
			# for valor in destinos.dest_list().items():
				print(valor)
		# Fecha programa
		elif cmd[0] == 'quit':
			ligado = False

		# else:
			# print('comando invavido')

# Envia o pacote 'update' com intervalo predefinido
def envia_custos():
	global tempo, tout, ligado, HOST, PORT
	contador = 0
	while ligado:
		if tempo+tout < time():
			tempo = time()
			viz = destinos.viz_list()
			viz.remove(HOST)
			# print (json.dumps(destinos.destinos, indent=4))

			# Manda para cada vizinho os destinos que nao vieram dele
			for v in viz:
				dest = destinos.dest_list(v)
				# del dest[HOST]
				if dest:
					pac = {
					"type": "update",
					"source": HOST,
					"distances": dest,
					"destination": v
					}
					pacote = json.dumps(pac)
					udp.sendto(pacote.encode('latin1'), (v, PORT))
					# print(pacote)

			t_list = destinos.list_timeout(4*tout)
			for v in t_list:
				destinos.viz_del(v)


# Trata pacotes recebidos
def recebe():
	global ligado, HOST, PORT
	while ligado:
		# Recebe pacote de ata 64kb
		pacote, addr = udp.recvfrom(1024)
		pac = json.loads(pacote.decode('latin1'))
		# print ("recived: ",addr[0])
		v = addr[0]
		if pac['type'] == 'update':
			if pac ["destination"] == HOST:
				destinos.dest_update(pac['distances'], v)

		elif pac['type'] == 'trace':
			pac['hops'].append(HOST)
			if pac['destination'] == HOST:
				dest = destinos.viz_to_dest(pac['source'])
				if dest:
					rpac = {
					"type": "data",
					"source": HOST,
					"destination": pac['source'],
					"payload": pac
					}
					pacote = json.dumps(rpac)
					# print(pacote)
					udp.sendto(pacote.encode('latin1'), (dest, PORT))
				# else:
					# print(rpac['destination'], 'nao pode ser alcancado')
			else:
				dest = destinos.viz_to_dest(pac['destination'])
				if dest:
					pacote = json.dumps(pac)
					# print(pacote)
					udp.sendto(pacote.encode('latin1'), (dest, PORT))
				# else:
					# print(pac['destination'], 'nao pode ser alcancado')

		elif pac['type'] == 'data':
			if pac['destination'] == HOST:
				print (json.dumps(pac['payload'], indent=4))

			else:
				dest = destinos.viz_to_dest(pac['destination'])
				if dest:
					pacote = json.dumps(pac)
					# print(pacote)
					udp.sendto(pacote.encode('latin1'), (dest, PORT))
				# else:
					# print(pac['destination'], 'nao pode ser alcancado')


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
balanceamento = 1

destinos.viz_add(HOST, '0')
del destinos.tempo[HOST]

# Le inicializa por arquivos STARTUPs
if len(sys.argv) > 3:
	for arq in sys.argv[3:]:
		with open(arq, "r") as arq_start:
			for dest in arq_start.readlines():
				# print(dest)
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
