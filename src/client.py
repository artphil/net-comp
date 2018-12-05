'''
Universidade Federal de Minas Gerais
Trabalho pratico da disciplina Rede de Computadores da UFMG
Protocolo HTTP e servico REST
Arthur Phillip D. Silva 
Cliente
'''
import json
import socket
import sys
# import ssl

# Tamanho do pacote recebido
pack_size = 10000

# Recebe pacote tipo json
def get_api(ext):
	global dest

	# Abre conexao
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp.connect(dest)

	# Protocolo de seguranca
	# tcp = ssl.wrap_socket(tcp, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

	# Cabecalho de requisicao HTTP
	http = "GET "+ext+" HTTP/1.1\r\nHost: "+HOST+"\r\nAccept: */*\r\nConnection: Close\r\n\r\n" #

	# Envio do pacote 
	tcp.send(http.encode('latin1'))

	# Recebimento e montagem da mensagem
	pack = tcp.recv(pack_size)
	msg = ''
	while len(pack) > 0:
		msg += pack.decode('latin1')
		pack = tcp.recv(pack_size)

	# Fecha conexao
	tcp.close()

	# Separa Cabecalho da mensagem 
	head , msg_json = msg.split('{',1)
	
	return json.loads("{" + msg_json)

## Programa

# Leitura de argumentos
HOST, sPORT = sys.argv[1].split(":")
PORT = int(sPORT)
dest = (HOST, PORT)

OPT = int(sys.argv[2])

# Requisicao do 'IX'
ix = get_api("/api/ix")

# Resultado
data={}

# Tratamento de opcoes
if OPT == 0: # Quantos IX para cada NET
	for item in ix['data']:
		net = get_api("/api/ixnets/"+str(item['id']))
		for lan in net['data']:
			if lan['net_id'] in data:
				data[lan['net_id']]['num'] += 1
			else:
				data[lan['net_id']] = {}
				data[lan['net_id']]['num'] = 1
				name = get_api("/api/netname/"+str(lan['net_id']))
				data[lan['net_id']]['name'] = name['data'][0]

elif OPT == 1: # Quantos NET para cada IX
	for item in ix['data']:
		net = get_api("/api/ixnets/"+str(item['id']))
		data[item['id']] = {}
		data[item['id']]['name'] = item['name']
		if 'data' in net:
			data[item['id']]['num'] = len(net['data'])
		else:
			data[item['id']]['num'] = 0

# Imprime arquivo '.csv' para analise
p = False
if p: output = open('output'+str(OPT)+'.csv', 'w')

for kid, dat in data.items():
	print("{}	{}	{}".format(kid, dat['name'], dat['num']))
	if p: output.write("{};{};{};\n".format(kid, dat['name'], dat['num']))

if p: output.close()