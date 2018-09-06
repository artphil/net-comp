'''
 Universidade Federal de Minas Gerais
 Trabalho pratico da disciplina Rede de Computadores da UFMG
 Servidor UDP

 Arthur Phillip D. Silva & Gabriel Almeida de Jesus
'''
import socket
import sys
import crypt
from struct import pack, unpack, calcsize
from time import time
from hmac import compare_digest as compare_hash

'''
Chamada do programa

python server.py <arquivo> <port> <Wrx> <Perror>

arquivo	: caminho para gravar logs
port	: porto do servidor
Wrx		: tamanho da janela deslizante
Perror	: probabilidade de erro do md5 de confirmacao

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

# Imprime a janela deslizante
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


# Recebe e separa os Parametros Host e Port
HOST = ''					# Endereco IP do Servidor
PORT = int(sys.argv[2])		# Porta que o Servidor esta

# Recebendo parametros de Entrada
arquivo = sys.argv[1]
tamJanela = int(sys.argv[3])
probErro = float(sys.argv[4])

# Criando socket de comunicacao UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
orig = (HOST, PORT)
udp.bind(orig)

# Grava log
arq_log = open(arquivo, 'w')

# Tratamento de conversas e suas janelas
cliente_list = {}

# Execucao do programa
while True:
	# Espera contato
	pacote, cliente = udp.recvfrom(1024)

	# secciona pacote em variaveis
	parte = pacote[:calcsize('L')]
	msg_id = unpack('L', parte)[0]
	pacote = pacote[calcsize('L'):]

	parte = pacote[:calcsize('L')]
	seg = unpack('L', parte)[0]
	pacote = pacote[calcsize('L'):]

	parte = pacote[:calcsize('I')]
	nseg = unpack('I', parte)[0]
	pacote = pacote[calcsize('I'):]

	parte = pacote[:calcsize('H')]
	tam = unpack('H', parte)[0]
	pacote = pacote[calcsize('H'):]

	parte = pacote[:tam]
	msg = parte.decode('latin1')
	pacote = pacote[tam:]

	mhash = pacote.decode('latin1')
	chash = crypt.crypt(str(msg_id)+str(seg)+str(nseg)+str(tam)+msg, mhash)

	# Verifica integridade do pacote
	if compare_hash(mhash, chash):
		#TODO: enviar confirmacao
		rhash = crypt.crypt(str(msg_id)+str(seg)+str(nseg), crypt.METHOD_MD5)
		udp.sendto(pack('L', msg_id)+pack('L', seg)+pack('I', nseg)+rhash.encode('latin1'), cliente)

		# Verifica se eh nova conexao
		if cliente not in cliente_list:
			cliente_list[cliente] = {}
			cliente_list[cliente]['janela'] = {}
			cliente_list[cliente]['gravar'] = 0
			cliente_list[cliente]['gravado'] = []

		# Atualiza ultimo contado com cliente
		cliente_list[cliente]['tempo'] = time()

		# Verifica se a mensagem ja esta na janela
		if msg_id not in cliente_list[cliente]['janela']:
			# Verifica se a janela esta cheia
			if len(cliente_list[cliente]['janela']) < tamJanela:
				# Verifica se a mensagem esta dentro do escopo da janela
				if msg_id >= cliente_list[cliente]['gravar'] and msg_id < (cliente_list[cliente]['gravar']+tamJanela):
					cliente_list[cliente]['janela'][msg_id] = {}
					cliente_list[cliente]['janela'][msg_id]['seg'] = seg
					cliente_list[cliente]['janela'][msg_id]['nseg'] = nseg
					cliente_list[cliente]['janela'][msg_id]['msg'] = msg
					cliente_list[cliente]['janela'][msg_id]['mhash'] = mhash

	# Salva todas as mensagens posssiveis no arquivo respeitando a ordem
	for k, v in cliente_list.items():
		# Grava as mensagens e as marca
		for k1, v1 in v['janela'].items():
			if v['gravar'] == k1:
				arq_log.write(v1['msg']+'\n')
				v['gravado'].append(v['gravar'])
				v['gravar'] += 1
		# Deleta as mensagens ja gravadas
		while v['gravado']:
			n = v['gravado'][0]
			del v['janela'][n]
			del v['gravado'][0]


	dprint(cliente_list)

udp.close()
