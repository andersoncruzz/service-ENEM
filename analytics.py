def analytics(user, sumarioL, idView):

	for line in sumarioL:
		listDataLastLine = line.split(";")	
		if user == listDataLastLine[0] and int(listDataLastLine[2]) > 60000 and idView != "" and idView[0] == "Q":
			#print "ADPTACAO NO CONTEUDO, MAIS DE 7 SEGUNDOS SEM INTERACAO"
			return True				
	return False 
