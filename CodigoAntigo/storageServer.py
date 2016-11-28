#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
#from flask.ext.cors import CORS, cross_origin
from sumario import LoadSummarizer, analytics
import os
import thread
import time
import threading

app = Flask('storage')
CORS(app)
#moveBufferHttpRest_to_BufferChangeLogger = False
#Criando diretório sessions caso não exista	
if os.path.exists("sessions-bufferHTTPRest") == False:
	os.makedirs("sessions-bufferHTTPRest")

if os.path.exists("bufferChangerLogger") == False:
	os.makedirs("bufferChangerLogger")
#Guarda em memória as sessões ativas

#semaforo_sumarizerLog = True
active_sessions = list()
#recomendationUsers = list()
active_sessions.append("1")

#def moduleSummarizer():
	#while True:
		#time.sleep(5)
		#print "sumarizer: " 
		#print active_sessions
		#print "thread it's working"
		#if semaforo_sumarizerLog == True:
		#	semaforo_sumarizerLog = False
		#	semaforo_sumarizerLog = LoadSummarizer(active_sessions)	
		
		#time.sleep(3)
		#if semaforo_sumarizerLog == True:
		#	semaforo_sumarizerLog = False
		#	recomendationUsers = analytics(active_sessions)

def moduleSummarizer(user, timestamp, session):
	#LoadSummarizer(active_sessions)
	recomendationUser = analytics(user, timestamp, session)	
	return recomendationUser

def moveBufferHttpRest_to_BufferChangeLogger():
#	moveBufferHttpRest_to_BufferChangeLogger = True
	while True:
		time.sleep(10)
		#print "thread it's working"
		for session in active_sessions:
			for file in os.listdir("sessions-bufferHTTPRest/000"+session):
				if file.endswith(".csv"):
					if os.path.exists("bufferChangerLogger/000"+session) == False:
						os.makedirs("bufferChangerLogger/000"+session)
					#os.rename("sessions-bufferHTTPRest/000"+session+"/"+file, "bufferChangerLogger/000"+session+"/"+file)
					filebufferChangeLogger = open("bufferChangerLogger/000"+session+"/"+file, "a+")
					filebufferHTTPRest = open("sessions-bufferHTTPRest/000"+session+"/"+file)
					filebufferChangeLogger.write(filebufferHTTPRest.read())
					filebufferHTTPRest.close()
					filebufferChangeLogger.close()
					os.remove("sessions-bufferHTTPRest/000"+session+"/"+file)
					
				#print("session"+session+ " file"+file)
			#moveBufferHttpRest_to_BufferChangeLogger = False
			#time.sleep(5)

@app.route("/storage/<idSession>", methods=["POST"])
def receive_data(idSession):
	if request.method == "POST":
		if verify_active_session(idSession) == False:
			create_session(idSession)
		idUser = request.form["idUser"]					
		event = request.form["tipo"]		
		resource = request.form["tag"]
		timestamp = request.form["timeStamp"]
		x = request.form["x"]
		y = request.form["y"]
		idView = request.form["id"]    	

	#Tupla está sendo escrito no arquivo em formato CSV
		data_received =	"000"+idSession+";000"+idUser+";"+timestamp+";"+event +";"+idView+";"+resource+";"+x+";"+y+"\n"

		fileBuffer = open("sessions-bufferHTTPRest/000"+idSession+"/000"+idUser+"_cache.csv", "a")	
		fileBuffer.write(data_received)
		fileBuffer.close()	
		print "000"+idSession+";000"+idUser+";"+timestamp+";"+event +";"+idView+";"+resource+";"+x+";"+y
		#response = flask.jsonify({'retorno': 'Evento recebido.'})
		#response.headers.add('Access-Control-Allow-Origin', '*')		
		return "ok", 200

@app.route("/analytics/<idSession>", methods=["GET"])
def receiveAnalytics(idSession):
	if request.method == "GET":
		idUser = request.args.get("idUser")
		timeStamp = request.args.get("timestamp")
		#print "idUser" + idUser				
		if moduleSummarizer(idUser, timeStamp, idSession) == True:
			return "True", 200
		else:
			return "False", 200

#Cria diretório que representa a sessão
def create_session(idSession):
	if os.path.exists("sessions-bufferHTTPRest/000"+idSession) == False:
		os.makedirs("sessions-bufferHTTPRest/000"+idSession)
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
	#ThreadmoveBufferHttpRest_to_BufferChangeLogger = threading.Thread(target=moveBufferHttpRest_to_BufferChangeLogger)
	#ThreadmoveBufferHttpRest_to_BufferChangeLogger.start()
	#ThreadmoveBufferHttpRest_to_BufferChangeLogger.join()	
	#ThreadSummarizer = threading.Thread(target=moduleSummarizer)
	#ThreadSummarizer.start()
	#ThreadSummarizer.join()	
	app.run(debug=True, host='0.0.0.0')
	#@crossdomain(origin='*')