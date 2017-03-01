 
def LoadSummarizerByUser(user, timestamp, event, idView, sumarioL):
	#Percorre o sumario atras do usuario
	exemplo = sumarioL
	#print "exemplo"
	#print exemplo
	t = []
	i = 0
	if sumarioL:
		#print "if"
		for line in sumarioL:
			#print "for"
			listDataLine = line.split(";")
			if user == listDataLine[0]:
				#print "if1"
				t = listDataLine
				break	
			i += 1 
		if(t == []):
			#print "if2"
			Delta = "0"
			Data = user + ";" + timestamp + ";" + Delta + ";" + idView		
			#print "Data"
			#print Data
			exemplo.append(Data)
		else:
			#print "else"
			if(event == "click"):
				#print "if3"
				Delta = "0"
				Data = user + ";" + timestamp + ";" + Delta + ";" + idView	
			else:
				#print "else2"
				Delta = str(int(timestamp) - int(t[1]))
				Data = user + ";" + t[1] + ";" + Delta + ";" + idView
				#print Data
			exemplo[i] = Data
	else:
		#print "else3"
		Delta = "0"
		Data = user + ";" + timestamp + ";" + Delta + ";" + idView		
		#print "Data"
		#print Data
		exemplo.append(Data)
	return exemplo	

def ClearSummarizerByUser(idUser, event, timestamp, idView, sumarioL):
	print "na funcao"
	if sumarioL == []:
		aux_str = idUser + ";" + timestamp + ";" + 0 + ";" + idView
		sumarioL.append(aux_str)
		return sumarioL

	if event == "click":
		listAux = list()
		for i in sumarioL:
			aux = i.split(";")
			if aux[0] == idUser:
				aux_str = aux[0] + ";" + timestamp + ";" + 0 + ";" + idView
				listAux.append(aux_str)
			else:
				listAux.append(i)
		return listAux
	return sumarioL


def LoadQuestionTime (user, timeQuestions, idQuestion, timestamp):
	
	flagUserExists = False
	#Verificando se o usuario existe na lista do timeQuestions
	for userActives in timeQuestions:
		if userActives[0][0] == user:
			flagUserExists = True
		#adicionando na lista do recomender este usuario
	if flagUserExists == False:
		#print "if"
		timeQuestions.append([[user, idQuestion], [0,0,0], [0,0,0], [0,0,0]])

	if len(timeQuestions) > 0:
		i = 0
		for userActives in timeQuestions:
			if userActives[0][0] == user:
				if userActives[0][1] == idQuestion:
					if userActives[idQuestion][0] == 0:
						userActives[idQuestion][0] = timestamp	
					else:
						userActives[idQuestion][1] = (timestamp - userActives[idQuestion][0] + userActives[idQuestion][1])
						userActives[idQuestion][0] = timestamp
						userActives[idQuestion][2] = (userActives[idQuestion][1])/1000.0 
				else:
					userActives[idQuestion][0] = timestamp
					userActives[0][1] = idQuestion	
				#print userActives 	
		#print ""					
		#print feedback
		return timeQuestions

#print LoadSummarizerByUser("0001", "2000", "null", "conteudo", [])
#print LoadSummarizerByUser("0002", "9000", "null", "conteudo", ['0001;2000;0;conteudo'])
#print LoadSummarizerByUser("0001", "10000", "null", "conteudo", ['0001;2000;0;conteudo', '0002;9000;0;conteudo'])