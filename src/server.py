'''
Universidade Federal de Minas Gerais
Trabalho pratico da disciplina Rede de Computadores da UFMG
Protocolo HTTP e servico REST
Arthur Phillip D. Silva 
Servidor
'''
import json
import sys
from flask import Flask, Response

# Inicia flask
app = Flask(__name__)

# tratamento das api's
@app.route("/api/ix") # Retorna o arquivo IX inteiro 
def api_ix():
	response = Response(
		response = json.dumps(json_ix, default=lambda o: o.__dict__),
		status = 200,
		mimetype = 'application/json'
	)
	return response

@app.route("/api/ixnets/<int:ix_id>") # Retorna  de NET's para o IX fornecido
def api_netixlan(ix_id):
	data = {'meta':{}, 'data':[]}
	for edge in json_lan['data']:
		if edge['ix_id'] == ix_id:
			data['data'].append(edge)

	return Response(
		response = json.dumps(data, default=lambda o: o.__dict__),
		status = 200,
		mimetype = 'application/json'
	)

@app.route("/api/netname/<int:net_id>") # Retorna nome da NET fornecida
def api_net(net_id):
	data = {'meta':{}, 'data':[]}
	for edge in json_net['data']:
		if edge['id'] == net_id:
			data['data'].append(edge["name"])
			break
	
	return Response(
		response = json.dumps(data, default=lambda o: o.__dict__),
		status = 200,
		mimetype = 'application/json'
	)

## Programa 

# Importa json dos arquivos
with open('ix.json', 'r') as arq: 
	json_ix = json.load(arq)

with open('net.json', 'r') as arq: 
	json_net = json.load(arq)

with open('netixlan.json', 'r') as arq: 
	json_lan = json.load(arq)

# Inicia servidor
app.run(port=int(sys.argv[1]), use_reloader=True)
