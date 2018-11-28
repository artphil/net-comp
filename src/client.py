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

tam_max = 1024


def get_json(api):
	global dest
	t = time()

	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp.connect(dest)
	tcp = ssl.wrap_socket(tcp, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)

	http = "GET "+api+" HTTP/1.1\r\nHost: "+HOST+"\r\nAccept: */*\r\nConnection: Close\r\n\r\n" #

	tcp.send(http.encode('latin1'))

	resp = tcp.recv(tam_max).decode('latin1')
	txt = ''
	while len(resp)>0:
		txt += resp
		resp = tcp.recv(tam_max).decode('latin1')

	tcp.close()
	print("\n", txt)
	head = txt.split('{')[0]
	return json.loads(txt[len(head):])



HOST, P = sys.argv[1].split(":")
OPT = int(sys.argv[2])
PORT = int(P)

dest = (HOST, PORT)

ix = get_json("/api/ix") #modificar para /api/ixids

if OPT == 1:
	ix_nets = {}
	for rede in ix['data']:
		print(rede['id'])
		net = get_json("/api/ixlan/"+str(rede['id']))
		ix_nets[rede['id']] = {}
		ix_nets[rede['id']]['nome'] = rede['name']
		if 'data' in net:
			ix_nets[rede['id']]['n_nets'] = len(net['data'])
		else:
			ix_nets[rede['id']]['n_nets'] = 0
	print(json.dumps(ix_nets, indent=True))

	for id in ix_nets:
		print("{}	{}	{}".format(id, ix_nets[id][nome], ix_nets[id][n_nets]))
