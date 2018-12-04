'''
Universidade Federal de Minas Gerais
Trabalho pratico da disciplina Rede de Computadores da UFMG
Protocolo HTTP e servico REST
Arthur Phillip D. Silva & Gabriel Almeida de Jesus
Cliente
'''
import json
import socket
import ssl
import sys

MAX_TAM = 1024

def get_json(api):
	global dest

	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp.connect(dest)
	# tcp = ssl.wrap_socket(tcp, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

	http = "GET "+api+" HTTP/1.1\r\nHost: "+HOST+"\r\nAccept: */*\r\nConnection: Close\r\n\r\n" #

	tcp.send(http.encode('latin1'))

	resp = tcp.recv(MAX_TAM).decode('latin1')
	txt = ''
	while len(resp)>0:
		txt += resp
		resp = tcp.recv(MAX_TAM).decode('latin1')

	tcp.close()
	head = txt.split('{',1)[0]
	print(http, "\n", head, "\n")
	return json.loads(txt[len(head):])

def get_txt(api):
	global dest

	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp.connect(dest)

	http = "GET "+api+" HTTP/1.1\r\nHost: "+HOST+"\r\nAccept: */*\r\nConnection: Close\r\n\r\n" #

	tcp.send(http.encode('latin1'))

	resp = tcp.recv(MAX_TAM).decode('latin1')

	return resp

HOST, P = sys.argv[1].split(":")
OPT = int(sys.argv[2])
PORT = int(P)

dest = (HOST, PORT)

ix = get_json("/api/ix")
# netixlan = get_json("/api/netixlan")
# net = get_json("/api/net")

dados={}
data=[]
if OPT == 0:
	# for lan in netixlan['data']:
	# 	# if lan['ix_id'] == ix_fonec:
	# 	# 	data.append(lan)
	# 	if lan['net_id'] not in dados:
	# 		dados[lan['net_id']] = {}
	# 		dados[lan['net_id']]['num'] = []
	# 	if lan['ix_id'] not in dados[lan['net_id']]['num']:
	# 		dados[lan['net_id']]['num'].append(lan['ix_id'])
	# for n in net['data']:
	# 	if n['id'] in dados:
	# 		dados[n['id']]['nome'] = n['name']

	for rede in ix['data']:
		net = get_json("/api/ixnets/"+str(rede['id']))
		for lan in net['data']:
			if lan['id'] in dados:
				dados[lan['id']]['num'] += 1
			else:
				dados[lan['id']] = {}
				dados[lan['id']]['num'] = 1

	for id in dados:
		dados[id]['nome'] = get_txt("/api/netname/"+str(id))

if OPT == 1:
	# for lan in netixlan['data']:
	# 	if lan['ix_id'] not in dados:
	# 		dados[lan['ix_id']] = {}
	# 		dados[lan['ix_id']]['num'] = []
	# 	if lan['net_id'] not in dados[lan['ix_id']]['num']:
	# 		dados[lan['ix_id']]['num'].append(lan['net_id'])
	# for n in ix['data']:
	# 	if n['id'] in dados:
	# 		dados[n['id']]['nome'] = n['name']

	for rede in ix['data']:
		print(rede['id'])
		net = get_json("/api/ixnets/"+str(rede['id']))
		dados[rede['id']] = {}
		dados[rede['id']]['nome'] = rede['name']
		if 'data' in net:
			dados[rede['id']]['num'] = len(net['data'])
		else:
			dados[rede['id']]['num'] = 0

# sort(dados)
for k, v in dados.items():
	print("{}	{}	{}".format(k, v['nome'], v['num']))
