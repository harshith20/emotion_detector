import sqlite3 as sql

def insertUser(username,password):
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username FROM users where username=(?)",(username))
	my_result = cur.fetchone()
	if my_result is None:
		cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
		con.commit()
		con.close()
	else:
		print('username already exists')	

	

def retrieveUsers():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	con.close()
	return users