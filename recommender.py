from datetime import *

def recommender (user, recommender, idQuestion, timestamp):
	
	flagUserExists = False
	#Verificando se o usuario existe na lista do recommender
	#print "recommender 1"
	for userActives in recommender:
		if userActives[0][0] == user:
			flagUserExists = True
		#adicionando na lista do recomender este usuario
	if flagUserExists == False:
		#print "if"
		recommender.append([[user, timestamp, "Q1-hard,Q2-hard,Q3-hard,Q4-hard,Q5-hard,Q6-hard,Q7-hard,Q8-hard,Q9-hard,Q10-hard"], [[False,False,False,False], [False,False,False,False],["0"], ["Q1-hard"]],[[False,False,False,False], [False,False,False,False], ["0"], ["Q2-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q3-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q4-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q5-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q6-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q7-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q8-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q9-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q10-hard"]]])
	#print "recommender 2"
	#print "BTN :" + btnTroca	
	if len(recommender) > 0:
		#print "recommender 3"
		#i = 0
		#recommendation = "ok"
		#gerando a recomendacao para o usuario
		for userActives in recommender:
			if userActives[0][0] == user:
				#Nao passou pela questao facil
				#print "recommender 4"
				if userActives[idQuestion][1][0] == True:
					#recommendation = "ok"
					print "Esta Questao ja utilizou todas as adaptacoes"				
				elif timestamp - userActives[0][1] > 7000: 
					userActives[0][1] = timestamp		
					if userActives[idQuestion][0][0] == False:
						if userActives[idQuestion][0][1] == False:
							userActives[idQuestion][0][1] = True
							print "D"+str(idQuestion)+"-hard;"								
							recommendation = "D"+str(idQuestion)+"-hard" + ";"
							userActives[idQuestion][3][0] = recommendation
							questions = userActives[0][2]
						elif userActives[idQuestion][0][2] == False:
							userActives[idQuestion][0][2] = True
							print "C"+str(idQuestion)+"-hard"	
							recommendation = "D"+str(idQuestion)+"-hard" + ";" + "C"+str(idQuestion)+"-hard" + ";"
							userActives[idQuestion][3][0] = recommendation
							questions = userActives[0][2]
						elif userActives[idQuestion][0][3] == False:
							userActives[idQuestion][0][3] = True
							#Vai passar para questao facil	
							userActives[idQuestion][0][0] = True
							print "Q"+str(idQuestion)+"-easy"
							recommendation = "D"+str(idQuestion)+"-hard" + ";" + "C"+str(idQuestion)+"-hard" + ";" + "Q"+str(idQuestion)+"-easy" + ";"
							userActives[idQuestion][3][0] = recommendation
							questions = userActives[0][2]
					else:
						if userActives[idQuestion][1][0] == False: 
							if userActives[idQuestion][1][1] == False and userActives[idQuestion][2][0] == "1":
								userActives[idQuestion][1][1] = True
								print "D"+str(idQuestion)+"-easy;"	
								recommendation = "D"+str(idQuestion)+"-easy" + ";"
								userActives[idQuestion][3][0] = recommendation
								questions = userActives[0][2]
							elif userActives[idQuestion][1][2] == False and userActives[idQuestion][2][0] == "1":
								userActives[idQuestion][1][2] = True
								print "C"+str(idQuestion)+"-easy"	
								recommendation = "D"+str(idQuestion)+"-easy" +";" +"C"+str(idQuestion)+"-easy" + ";"
								userActives[idQuestion][3][0] = recommendation
								questions = userActives[0][2]
							elif userActives[idQuestion][1][3] == False and userActives[idQuestion][2][0] == "1":
								#userActives[idQuestion][1][3] = True
								#Vai passar para questao facil	
								#userActives[idQuestion][1][0] = True
								#print "P"+str(idQuestion)
								#recommendation = "D"+str(idQuestion)+"-easy" +";" +"C"+str(idQuestion)+"-easy" + ";" + "P"+str(idQuestion) + ";"								
								recommendation = userActives[idQuestion][3][0]
								questions = userActives[0][2]
							else:
								recommendation =  userActives[idQuestion][3][0]
								questions = userActives[0][2]
				else:
					#userActives[0][1] = -1
					#print "recommender 5"
					#print "Adptacao OKKK"
					recommendation = userActives[idQuestion][3][0]
					questions = userActives[0][2]
					#print "Enviamos uma adaptacao ha pouco tempo"


		#print ""
		#userActives[0][2] = recommendation	
		dt = datetime.now()
		strTimeDate = str(dt.day) + "/" + str(dt.month) + "/" + str(dt.year) + "-" + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second) + "-" + user+";"+str(recommendation) + "\n"
		logService = open("SERVICE_log.csv", "a+")
		logService.write(strTimeDate)
		logService.close()

		feedback = []
		feedback.append(recommender)
		feedback.append(recommendation)
		feedback.append(questions)
		#print "recommender 6"
		#print feedback
		return feedback 																

def lastRecommendation (user, recommender, idQuestion, timestamp):
	flagUserExists = False
	#print "last 1"
	#Verificando se o usuario existe na lista do recommender
	for userActives in recommender:
		if userActives[0][0] == user:
			flagUserExists = True
		#adicionando na lista do recomender este usuario
	if flagUserExists == False:
		#print "if"
		recommender.append([[user, timestamp, "Q1-hard,Q2-hard,Q3-hard,Q4-hard,Q5-hard,Q6-hard,Q7-hard,Q8-hard,Q9-hard,Q10-hard"], [[False,False,False,False], [False,False,False,False],["0"], ["Q1-hard"]],[[False,False,False,False], [False,False,False,False], ["0"], ["Q2-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q3-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q4-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q5-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q6-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q7-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q8-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q9-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q10-hard"]]])

	#print "last 3"
	#print "BTN :" + btnTroca	
	if len(recommender) > 0:
		i = 0
		#print "last 3"
		for userActives in recommender:
			if userActives[0][0] == user:
				#Nao passou pela questao facil
				recommendation =  userActives[idQuestion][3][0]
				questions = userActives[0][2]
				#print ""

		#print "last 4"		
		#print ""					
		feedback = []
		feedback.append(recommender)
		feedback.append(recommendation)
		feedback.append(questions)
		#print feedback
		return feedback

def changeBtnQuestionEasy(user, recommender, idQuestion, timestamp):
	flagUserExists = False
	#print "change 1"
	#Verificando se o usuario existe na lista do recommender
	for userActives in recommender:
		if userActives[0][0] == user:
			flagUserExists = True
		#adicionando na lista do recomender este usuario
	#print "change 2"
	if flagUserExists == False:
		#print "if"
		recommender.append([[user, timestamp, "Q1-hard,Q2-hard,Q3-hard,Q4-hard,Q5-hard,Q6-hard,Q7-hard,Q8-hard,Q9-hard,Q10-hard"], [[False,False,False,False], [False,False,False,False],["0"], ["Q1-hard"]],[[False,False,False,False], [False,False,False,False], ["0"], ["Q2-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q3-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q4-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q5-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q6-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q7-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q8-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q9-hard"]],[[False,False,False,False], [False,False,False,False],["0"], ["Q10-hard"]]])
	#print "change 3"
	#print "BTN :" + btnTroca	
	if len(recommender) > 0:
		i = 0
		#print "change 4"
		for userActives in recommender:
			if userActives[0][0] == user:
				#Nao passou pela questao facil
				userActives[idQuestion][2][0] = "1"
				questions =  userActives[0][2]
				questions = questions.split(",")
				questions[idQuestion-1] = "Q"+ str(idQuestion) + "-easy"
				aux = ""
				for i in questions:
				#questions = questions[0] + "," + questions[1] + "," + questions[2]
					aux = aux+ "," + i
				questions = aux[1:]
				userActives[0][2] = questions
				userActives[idQuestion][3][0] = "Q"+ str(idQuestion) + "-easy"
				#userActives[idQuestion][3][0] = "ok"
				recommendation =  userActives[idQuestion][3][0]
				#print ""


		#print ""		
		#print "change 5"			
		feedback = []
		feedback.append(recommender)
		feedback.append(recommendation)
		feedback.append(questions)
		#print feedback
		return feedback
