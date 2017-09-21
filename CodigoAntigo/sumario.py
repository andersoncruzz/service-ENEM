import os
import csv
import time
import thread
import datetime
import fileinput

def updateDataUser(path, lineOld, lineNew):
	f = open(path,'r')
	filedata = f.read()
	f.close()

	newdata = filedata.replace(lineOld, lineNew)

	f = open(path,'w')
	f.write(newdata)
	f.close()

def updateStateUser(path, user, lineNew):
	#Verificando se o usuario esta ativo no sumarizador
	if (os.path.isfile(path)):
		fileSumarizer = open(path, "r+")
		#Pega a linha que pertence o usuario no arquivo
		for line in fileSumarizer:
			#print line 	
			listDataLastLine = line.split(";")
			#print "list: "+listDataLastLine[0]
			#print "user: "+user			
			if listDataLastLine[0] == user:
				#print "sim porra"
				fileSumarizer.close()
				updateDataUser(path, line, lineNew)			
				#print "\n\n"
				return True
		fileSumarizer.close()
	#Caso o usuario nao possua nenhuma linha no arquivo, significa que eh primeira vez sendo contabilizado no sumarizador
	#print "PQP"
	fileSumarizer = open(path, "a")
	fileSumarizer.write(lineNew)
	fileSumarizer.close()	

def LoadSummarizer(active_sessions):
	#print active_sessions
	for session in active_sessions:
		for file in os.listdir("sessions-bufferHTTPRest/000"+session):
			if file.endswith(".csv"):
				with open("sessions-bufferHTTPRest/000"+session+"/"+file) as f:
					lines = f.readlines()
					last_line = lines[-1] #pega ultima linha
					listDataLastLine = last_line.split(";") #transforma ultima linha em uma lista					
					#+"555" porque o timestamp vindo do JS pega os MS, no python ainda 
					#nao conseguir pega os MilliSegundos, so ate Segundos
					#para fazer subrtracao decidi completar com +555					
					if(listDataLastLine[3] == "click"):
						timestampAtual = int(str(int(time.time())) + "555") 
						DeltaS = timestampAtual - int(listDataLastLine[2]) #pega o timeStamp ultimo click do arquivo do aluno
						#print listDataLastLine

										    #idUser 									     idView
						data_sumarizer = listDataLastLine[1] + ";"+ DeltaS + ";" + listDataLastLine[4] + "\n"							
						#print "data_sumarizer: "+ data_sumarizer
						updateStateUser("sessions-bufferHTTPRest/000"+session+"/sumarizer.log", listDataLastLine[1], data_sumarizer)
	return True	

def LoadSummarizerByUser(user, session, timestamp):
	#print active_sessions
		with open("sessions-bufferHTTPRest/000"+session+"/"+user+"_cache.csv") as f:
			lines = f.readlines()
			last_line = lines[-1] #pega ultima linha
			listDataLastLine = last_line.split(";") #transforma ultima linha em uma lista					
			if(listDataLastLine[3] == "click"):
				DeltaS = int(timestamp) - int(listDataLastLine[2]) #pega o timeStamp ultimo click do arquivo do aluno
				print "Tempo sem interacao: "+str(DeltaS)
				#print listDataLastLine
									#idUser 						idView
				data_sumarizer = listDataLastLine[1] + ";"+ str(DeltaS) + ";" + listDataLastLine[4] + "\n"							
				updateStateUser("sessions-bufferHTTPRest/000"+session+"/sumarizer.log", listDataLastLine[1], data_sumarizer)
		return True




def analytics(user, timestamp, session):
	#print active_sessions
	#print "timeStamp GET: " + timestamp
	LoadSummarizerByUser(user, session, timestamp)
	#for file in os.listdir("sessions-bufferHTTPRest/000"+session):
		#if file.endswith(".log"):
			#print "session "+session
	fileSumarizer = open("sessions-bufferHTTPRest/000"+session+"/sumarizer.log", "r+")
			#Pega a linha que pertence o usuario no arquivo
	for line in fileSumarizer:
				#print "aqui1"
				#print line 	
		listDataLastLine = line.split(";")
				#print int(listDataLastLine[1])
				#DS = int(timestamp) - int(listDataLastLine[1])  
				#print "timestamp: "+ timestamp
		#print "timeStampSumarizer: "+ listDataLastLine[1]						
				#print DS		
		if user == listDataLastLine[0] and int(listDataLastLine[1]) > 7000 and listDataLastLine[2]!="conteudo":
				print "ADPTACAO NO CONTEUDO, MAIS DE 7 SEGUNDOS SEM INTERACAO"
				return True
	#print "RECOMENDATION FALSE"				
	return False 

#LoadSummarizer(["1"])
#print analytics(["1"])					
