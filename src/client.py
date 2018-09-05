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
from struct import pack
from time import time

'''
Chamada do programa

python client.py <arquivo> <IP>:<port> <Wtx> <Tout> <Perror>

arquivo	: para leitura das mensagens
IP		: ip do servidor
port	: porto do servidor
Wtx		: tamanho da janela deslizante
Tout	: tempo limite para reenvio
Perror	: probabilidade de erro do md5 de envio

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

# Criando socket de comunicacao UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (HOST, PORT)

# Tratamento de envio
msg_id = 0

janela = []

# Leitura da primeira linha do arquivo
arq = open(arquivo, 'r')
linha = arq.readline()
tempo = time()

# Execucao do programa
while linha or len(janela) > 0:
	# Composicao do pacote a enviar
	msg = linha[:-1]
	seg = int(tempo)
	nseg = int((tempo-seg)*1000000000)
	tam = len(msg)

	#TODO: colocar pacote sem hash em estrutura
	# Calculo hash do pacote
	mhash = crypt.crypt(str(msg_id)+str(seg)+str(nseg)+str(tam)+msg, crypt.METHOD_MD5)
	print (mhash)

	#TODO: enviar todos pacotes novos ou com time out
	# Envio do pacote + hash
	udp.sendto(pack('L', msg_id)+pack('L', seg)+pack('I', nseg)+pack('H', tam)+msg.encode('latin1')+mhash.encode('latin1'), dest)

	#TODO: ler somente se tiver espaco na janela
	# Leitura de nova linha do arquivo
	linha = arq.readline()
	tempo = time()
	msg_id += 1

	#TODO: receber confirmacao
	#TODO: apagar confirmados da janela

arq.close()
udp.close()
