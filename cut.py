import csv
import os

def EscreveComplet(endereco, dados):
	arquivo_complet = open(endereco, "a")
	arquivo_complet.writelines(dados)
	arquivo_complet.close()

def EscreveBufferUsuario(endereco, dados):
	arquivo_user = open(endereco, "w")
	f = csv.writer(arquivo_user, delimiter = ';')
	f.writerows(dados)
	arquivo_user.close()

def LerBufferUsuario(endereco):
	with open(endereco) as f:
		lines = f.readlines()
	return(lines)

def GetLastClick(dados):
	lista_temporaria = [];
	for x in reversed(dados):
		elemento = x.split(";")
		if(elemento[3] == 'click'):
			lista_temporaria.append(elemento)
			break
	return lista_temporaria

def cut(user, session):

	endereco = "sessions-bufferHTTPRest/000"+session+"/"+user+"_cache.csv"
	dados_buffer_usuario = LerBufferUsuario(endereco)
	ultimoClick = [[]]
	if dados_buffer_usuario:
		ultimoClick = GetLastClick(dados_buffer_usuario)
		EscreveComplet("sessions-bufferHTTPRest/000"+session+"/complet.log", dados_buffer_usuario)
		EscreveBufferUsuario(endereco, [])
	return ultimoClick[0]

