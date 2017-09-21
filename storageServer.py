#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
from flask_cors import CORS, cross_origin
import os
import thread
import time
import threading
import sys, errno
from werkzeug import secure_filename
from datetime import *


app = Flask('storage', static_folder='realtime')
CORS(app)

#moveBufferHttpRest_to_BufferChangeLogger = False
#Criando diretório sessions caso não exista	
if os.path.exists("sessions-Logs") == False:
	os.makedirs("sessions-Logs")

@app.route('/')
def index():
    return render_template('index.html')

active_sessions = list()
active_sessions.append("1")


@app.route("/storage/<idSession>", methods=["POST"])
def receive_data(idSession):
	if request.method == "POST":
		try:
			if verify_active_session(idSession) == False:
				create_session(idSession)
			idUser = request.form["idUser"]					
			event = request.form["tipo"]		
			resource = request.form["tag"]
			timestamp = request.form["timeStamp"]
			x = request.form["x"]
			y = request.form["y"]
			tela = request.form["tela"]
			idView = request.form["classId"]    	
			
			if x == "" and y == "" and resource == "":
				#Neste bloco está sendo atualizado a última linha que significa o timestamp e a tela atual passado pelo Player
				with open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv", "a+") as f:
					lines = f.readlines()
					if len(lines) > 0:
						lineOld = lines[-1] #pega ultima linha
						lineNew = idSession+";"+idUser+";"+timestamp+";"+event +";"+ tela+ ";"+idView+";"+resource+";"+x+";"+y+"\n"
						f.close()

						fileaux = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv",'r')
						filedata = fileaux.read()
						fileaux.close()

						newdata = filedata.replace(lineOld, lineNew)

						fileaux = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv",'w')
						fileaux.write(newdata)
						fileaux.close()
					else:
						newdata = idSession+";"+idUser+";"+timestamp+";"+event +";"+ tela +";"+idView+";"+resource+";"+x+";"+y+"\n"
						fileaux = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv",'w')
						fileaux.write(newdata)
						fileaux.close()

			else:
				with open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv", "a+") as f:
					lines = f.readlines()
					lineOld = lines[-1] #pega ultima linha
					f.close()
					#print lines

					fileaux = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv",'r')
					filedata = fileaux.read()
					fileaux.close()

					dt = datetime.now()
					strTimeDate = str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year) + "-" + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)

					lineNew = strTimeDate + ";"+ idSession+";"+idUser+";"+timestamp+";"+event +";"+ tela +";"+idView+";"+resource+";"+x+";"+y+"\n"
					newdata = filedata.replace(lineOld, lineNew)
					newdata = newdata + lineOld 
					#print newdata
					fileaux = open("sessions-Logs/"+idSession+"/"+idUser+"_log.csv",'w')
					fileaux.write(newdata)
					fileaux.close()


			print idSession+";"+idUser+";"+timestamp+";"+event +";"+ tela +";"+idView+";"+resource+";"+x+";"+y
			print ""
			dt = datetime.now()
			strTimeDate = str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year) + "-" + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second) + "-" + idUser+";"+timestamp+";"+event +";"+ tela +";"+idView+";"+resource+";"+x+";"+y + "\n"
			logService = open("SERVICE_log.csv", "a+")
			logService.write(strTimeDate)
			logService.close()
			#print "btn Storage" + btnTroca[0]
			#Solicita recomendacao caso o aluno estiver em uma questao

			recommendation = [{"recommendation": "ok"}, {"questions": "nada"}]
			return jsonify({'recommendation': recommendation})

		except:
			print "Broken2"
			dt = datetime.now()
			strTimeDate = str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year) + "-" + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second) + "-" +idUser+";" + "Broken2" + "\n"
			logService = open("SERVICE_log.csv", "a+")
			logService.write(strTimeDate)
			logService.close()
			pass

#Cria diretório que representa a sessão
def create_session(idSession):
	if os.path.exists("sessions-bufferHTTPRest/"+idSession) == False:
		os.makedirs("sessions-bufferHTTPRest/"+idSession)
		active_sessions.append(str(idSession))
		print "Created the directoy:" +idSession

#Verifica em memória se a sessão está ativa
def verify_active_session(idSession):
	#print idSession
	#print active_sessions
	for session in active_sessions:
		if session == idSession:
			#print "The session is active"
			return True
	#print "The session isn't active"
	return False

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
