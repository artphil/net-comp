'''
 Universidade Federal de Minas Gerais
 Trabalho pratico da disciplina Rede de Computadores da UFMG
 Cliente UDP

 Arthur Phillip D. Silva & Gabriel Almeida de Jesus
'''

# Bibliotecas
import socket
import sys
import string
import crypt
import threading
from random import random
from struct import pack, unpack, calcsize
from hmac import compare_digest as compare_hash
from time import time

'''
Chamada do programa
python client.py <arquivo> <IP>:<port> <Wtx> <Tout> <Perror>

Variaveis
arquivo	: para leitura das mensagens
IP		: ip do servidor
port	: porto do servidor
Wtx		: tamanho da janela deslizante
Tout	: tempo limite para reenvio
Perror	: probabilidade de erro do md5 de envio

Formato da Janela Deslizante
DIAGRAMA 1: Formato de mensagens de log
0        8       16   20 22              22+sz            22+sz+16
+--------+--------+----+--+----/ ... /----+----------------+
|seqnum  |sec     |nsec|sz|message        |md5             |
+--------+--------+----+--+----/ ... /----+----------------+

DIAGRAMA 2: Formato de mensagens de confirmação (ack)
0        8       16   20               36
+--------+--------+----+----------------+
|seqnum  |sec     |nsec|md5             |
+--------+--------+----+----------------+
'''


''' Funcoes '''
# Verifica se deve haver erro
def ErroMD5 ():
	rand = random()
	print('\nrand: ', rand, 'erro', Perror, '\n')
	if rand < Perror:
		return True # Houve Erro
	else:
		return False # Nao Houve Erro

# Imprime a janela deslizante
def j_print ():
	j_lock.acquire()
	print('--------------Data----------------')
	for k, v in janela.items():
		print ('id:', k)
		for k1, v1 in v.items():
			print ('	', k1, '	:', v1)
	print()
	print('----------------------------------')
	j_lock.release()

# Gerenciamento de envio
def envia():
	global fim_arq

	# Leitura da primeira linha do arquivo
	msg_id = 0
	linha = arq.readline()
	tempo = time()

	# Envia pacotes
	while not fim_arq or len(janela) > 0:
		# print ('l', linha, 'j', len(janela))

		# Verifica se tem linha no arquivo
		if linha:
			# Popular janela
			if len(janela) < Wtx:
				# Composicao do pacote a enviar
				j_lock.acquire()
				janela[msg_id] = {}
				janela[msg_id]['msg'] = linha[:-1]
				janela[msg_id]['tam'] = len(linha)-1
				janela[msg_id]['tempo'] = 0
				janela[msg_id]['seg'] = 0
				janela[msg_id]['nseg'] = 0
				j_lock.release()

				# Leitura de nova linha do arquivo
				msg_id += 1
				linha = arq.readline()
		else :
			fim_arq = True


		j_lock.acquire()
		for m_id, v in janela.items():
			if time() > (v['tempo'] + Tout):
				v['tempo'] = time()
				v['seg'] = int(v['tempo'])
				v['nseg'] = int((v['tempo']-v['seg'])*100000000)

				# Calculo hash do pacote com a probabilidade de Erro
				data = str(m_id)+str(v['seg'])+str(v['nseg'])+str(v['tam'])+v['msg']

				if ErroMD5():
					mhash = crypt.crypt(data+'erro', crypt.METHOD_MD5)
					print('m errado', m_id)
				else:
					mhash = crypt.crypt(data, crypt.METHOD_MD5)
					print('m certo', m_id)

				# print (mhash)

				# Composicao do pacote
				pacote  = pack('L', m_id)
				pacote += pack('L', v['seg'])
				pacote += pack('I', v['nseg'])
				pacote += pack('H', v['tam'])
				pacote += v['msg'].encode('latin1')
				# Envio do pacote + hash
				udp.sendto(pacote+mhash.encode('latin1'), dest)
		j_lock.release()

		# print('envia:')
		# j_print()

	arq.close()


# Gerenciamento de confirmacao
def recebe():
	# Recebe confirmacao
	while (not fim_arq) or len(janela) > 0:
		# print ('a', fim_arq, 'j', len(janela))

		# Espera contato
		pacote, servidor = udp.recvfrom(1024)
		# print(pacote)
		print('recebe:')
		j_print()

		# secciona pacote em variaveis
		parte = pacote[:calcsize('L')]
		r_id = unpack('L', parte)[0]
		pacote = pacote[calcsize('L'):]

		parte = pacote[:calcsize('L')]
		r_seg = unpack('L', parte)[0]
		pacote = pacote[calcsize('L'):]

		parte = pacote[:calcsize('I')]
		r_nseg = unpack('I', parte)[0]
		pacote = pacote[calcsize('I'):]

		rhash = pacote.decode('latin1')
		chash = crypt.crypt(str(r_id)+str(r_seg)+str(r_nseg), rhash)

		# Libera mensagem confirmada da janela
		if compare_hash(rhash, chash):
			if r_id in janela:
				j_lock.acquire()
				del janela[r_id]
				j_lock.release()


''' Programa '''
# Recebe e separa os Parametros Host e Port
HostPort = sys.argv[2]
P_Host, P_Port = HostPort.split(':')

HOST = P_Host		# Endereco IP do Servidor
PORT = int(P_Port)	# Porta que o Servidor esta

# Recebendo parametros de Entrada
arquivo = sys.argv[1]
Wtx = int(sys.argv[3])
Tout = int(sys.argv[4])
Perror = float(sys.argv[5])

# Criando socket de comunicacao UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

# Tratamento de envio
arq = open(arquivo, 'r')
fim_arq = False

# Armazem de mensagens não confirmadas
janela = {}
# Gerenciador de concorrencia
j_lock = threading.Lock()

# Execucao do programa
e = threading.Thread(target=envia)
r = threading.Thread(target=recebe)

# Inicia as threads
e.start()
r.start()

# Espera retorno
e.join()
r.join()

udp.close()
