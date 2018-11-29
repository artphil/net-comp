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
from time import time

MAX_TAM = 1024


def get_json(api):
	global dest
	t = time()

	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp.connect(dest)
	tcp = ssl.wrap_socket(tcp, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

	http = "GET "+api+" HTTP/1.1\r\nHost: "+HOST+"\r\nAccept: */*\r\nConnection: Close\r\n\r\n" #

	tcp.send(http.encode('latin1'))

	resp = tcp.recv(MAX_TAM).decode('latin1')
	txt = ''
	while len(resp)>0:
		txt += resp
		resp = tcp.recv(MAX_TAM).decode('latin1')

	tcp.close()
	print("\n", txt)
	head = txt.split('{')[0]
	return json.loads(txt[len(head):])



HOST, P = sys.argv[1].split(":")
OPT = int(sys.argv[2])
PORT = int(P)

dest = (HOST, PORT)

ix = get_json("/api/ix") #modificar para /api/ixids
netixlan = get_json("/api/netixlan")
net = get_json("/api/net")

dados={}
if OPT == 0:
	for lan in netixlan['data']:
		if lan['net_id'] not in dados:
			dados[lan['net_id']] = {}
			dados[lan['net_id']]['num'] = []
		if lan['ix_id'] not in dados[lan['net_id']]['num']:
			dados[lan['net_id']]['num'].append(lan['ix_id'])
	for n in net['data']:
		if n['id'] in dados:
			dados[n['id']]['nome'] = n['name']


	# net_ix = {}
	# for rede in ix['data']:
	# 	net = get_json("/api/ixlan/"+str(rede['id']))
	# 	for lan in net['data']:
	# 		if lan['id'] in net_ix:
	# 			net_ix[lan['id']]['nome'] = lan['name']
	# 			net_ix[lan['id']]['n_ixps'] += 1
	#
	# 		else:
	# 			net_ix[lan['id']] = {}
	# 			net_ix[lan['id']]['nome'] = lan['name']
	# 			net_ix[lan['id']]['n_ixps'] = 1

if OPT == 1:
	for lan in netixlan['data']:
		if lan['ix_id'] not in dados:
			dados[lan['ix_id']] = {}
			dados[lan['ix_id']]['num'] = []
		if lan['net_id'] not in dados[lan['ix_id']]['num']:
			dados[lan['ix_id']]['num'].append(lan['net_id'])
	for n in ix['data']:
		if n['id'] in dados:
			dados[n['id']]['nome'] = n['name']
	# ix_nets = {}
	# for rede in ix['data']:
	# 	print(rede['id'])
	# 	net = get_json("/api/netixlan/"+str(rede['id']))
	# 	ix_nets[rede['id']] = {}
	# 	ix_nets[rede['id']]['nome'] = rede['name']
	# 	if 'data' in net:
	# 		ix_nets[rede['id']]['n_nets'] = len(net['data'])
	# 	else:
	# 		ix_nets[rede['id']]['n_nets'] = 0
	# print(json.dumps(ix_nets, indent=True))
# sort(dados)
for k, v in dados.items():
	print("{}	{}	{}".format(k, v['nome'], len(v['num'])))
