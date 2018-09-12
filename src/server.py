'''
 Universidade Federal de Minas Gerais
 Trabalho pratico da disciplina Rede de Computadores da UFMG
 Servidor UDP

 Arthur Phillip D. Silva & Gabriel Almeida de Jesus
'''
import socket
import sys
import crypt
from time import time
from random import random
from struct import pack, unpack, calcsize
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

''' Funcoes '''
# Verifica se deve ter erro
def ErroMD5 ():
	rand = random()
	print('\nrand: ', rand, 'erro', Perror, '\n')
	if rand < Perror:
		return True # Houve Erro
	else:
		return False # Nao Houve Erro

# Imprime a janela deslizante
def dprint():
	print('--------------Data----------------')
	for k, v in cliente_list.items():
		print (k)
		print ('	tempo	:', v['tempo'])
		print ('	gravado	:', v['gravar'])
		for k1, v1 in v['janela'].items():
			print ('	id:', k1)
			for k2, v2 in v1.items():
				print ('		', k2, '	:', v2)
		print()
	print('----------------------------------')


''' Programa '''
# Recebe e separa os Parametros Host e Port
HOST = ''					# Endereco IP do Servidor
PORT = int(sys.argv[2])		# Porto do Servidor

# Recebendo parametros de Entrada
arquivo = sys.argv[1]
Wrx = int(sys.argv[3])
Perror = float(sys.argv[4])

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

	# Verifica se eh nova conexao
	if cliente not in cliente_list:
		cliente_list[cliente] = {}
		cliente_list[cliente]['janela'] = {}
		cliente_list[cliente]['gravar'] = 0
		cliente_list[cliente]['gravado'] = []

	# Atualiza ultima tentativa de contado do cliente
	cliente_list[cliente]['tempo'] = time()

	# Verifica integridade do pacote
	# print(compare_hash(mhash, chash))
	if compare_hash(mhash, chash):
        # Verifica se a mensagem esta dentro do escopo da janela
        if msg_id < (cliente_list[cliente]['gravar']+Wrx):
            # Calcula hash do pacote com a probabilidade de Erro
            data = str(msg_id)+str(seg)+str(nseg)

            if ErroMD5():
                rhash = crypt.crypt(data+'erro', crypt.METHOD_MD5)
                print('r errado', msg_id)
            else:
                rhash = crypt.crypt(data, crypt.METHOD_MD5)
                print('r certo', msg_id)

                # Envia confirmacao
                confirmacao = pack('L', msg_id)
                confirmacao += pack('L', seg)
                confirmacao += pack('I', nseg)
                udp.sendto(confirmacao+rhash.encode('latin1'), cliente)

        # Verifica se a mensagem ja foi gravada
        if msg_id >= cliente_list[cliente]['gravar']:
            # Verifica se a mensagem ja esta na janela
            if msg_id not in cliente_list[cliente]['janela']:
                # Verifica se a janela esta cheia
                if len(cliente_list[cliente]['janela']) < Wrx:
                    # Insere a mensagem na janela do cliente
                    cliente_list[cliente]['janela'][msg_id] = {}
                    cliente_list[cliente]['janela'][msg_id]['seg'] = seg
                    cliente_list[cliente]['janela'][msg_id]['nseg'] = nseg
                    cliente_list[cliente]['janela'][msg_id]['msg'] = msg
                    cliente_list[cliente]['janela'][msg_id]['mhash'] = mhash

	# Apaga cliente ocioso por mais de 60s
	ociosos = []
	for k, v in cliente_list.items():
		if time() - v['tempo'] > 60:
			ociosos.append(k)
	for clt in ociosos:
		del cliente_list[clt]

	# Salva todas as mensagens posssiveis no arquivo respeitando a ordem
	for k, v in cliente_list.items():
		# Grava as mensagens e as marca
		for k1, v1 in v['janela'].items():
			if v['gravar'] == k1:
				arq_log.write(v1['msg']+'\n')
				v['gravado'].append(v['gravar'])
				v['gravar'] += 1
		# Deleta as mensagens marcadas
		while v['gravado']:
			n = v['gravado'][0]
			del v['janela'][n]
			del v['gravado'][0]

    # Imprime as janelas
	dprint()

udp.close()
