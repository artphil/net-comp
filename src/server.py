'''
Universidade Federal de Minas Gerais
Trabalho pratico da disciplina Rede de Computadores da UFMG
Protocolo HTTP e servico REST
Arthur Phillip D. Silva & Gabriel Almeida de Jesus
Servidor
'''
import json
import sys
from flask import Flask, Response

arq = open('ix.json', 'r')
ix = json.load(arq)
arq.close()

arq = open('net.json', 'r')
net = json.load(arq)
arq.close()

arq = open('netixlan.json', 'r')
lan = json.load(arq)
arq.close()


app = Flask(__name__)

@app.route("/api/ix")
def api_ix():
	response = Response(
		response = json.dumps(ix, default=lambda o: o.__dict__),
		status = 200,
		mimetype = 'application/json'
	)
	return response

@app.route("/api/ixnets/<int:ix_id>")
def api_netixlan(ix_id):
	lista = []
	resposta = {'meta':{}, 'data':[]}
	for conect in lan['data']:
		if conect['ix_id'] == ix_id:
			resposta['data'].append(conect.copy())
	response = Response(
		response = json.dumps(resposta, default=lambda o: o.__dict__),
		status = 200,
		mimetype = 'application/json'
	)
	return response

@app.route("/api/netname/<int:net_id>")
def api_net(net_id):
	resposta = {'meta':{}, 'data':[]}
	for conect in net['data']:
		if conect['id'] == net_id:
			resposta['data'].append(conect["name"])
			break
	response = Response(
		response = json.dumps(resposta, default=lambda o: o.__dict__),
		status = 200,
		mimetype = 'application/json'
	)
	return response

# Inicialização do Servidor
if __name__ == "__main__":
	app.run(port=int(sys.argv[1]), debug=False, use_reloader=True)
