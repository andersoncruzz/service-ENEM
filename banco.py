import sqlite3


def newTeacher(Nome, Email, Matricula, Senha):
	try:	
		conn = sqlite3.connect('openLab.db')
		cur = conn.cursor()
		
		cur.execute("""
		INSERT INTO teachers (idTeacher, Nome, Email, Password)
		VALUES (?,?,?,?)
		""", (Matricula, Nome, Email, Senha))

		#gravando no bd
		conn.commit()

		print('Dados inseridos com sucesso.')

		conn.close()
		return True
	except Exception:
		print("Erro")
		return False

def searchTeacher(Matricula, Senha):
	try:	
		conn = sqlite3.connect('openLab.db')
		cur = conn.cursor()
		
		cur.execute("""
		SELECT * FROM teachers;
		""")

		for linha in cur.fetchall():
			if (linha[0] == Matricula and linha[3] == Senha):
				break
		conn.close()
		return linha
	except Exception:
		print("Erro")
		return []

def UpdateTeacher(Nome, Email, Matricula, Senha):
	try:	
		conn = sqlite3.connect('openLab.db')
		cur = conn.cursor()
		
		cur.execute("""
		INSERT INTO teachers (idTeacher, Nome, Email, Password)
		VALUES (?,?,?,?)
		""", (Matricula, Nome, Email, Senha))

		#gravando no bd
		conn.commit()

		print('Dados inseridos com sucesso.')

		conn.close()
	except Exception:
		print("Erro")