import sqlite3

# create empty database
connection = sqlite3.connect("database.db")
# communicate with the database
cursor = connection.cursor()

# data to be inserted into the database
# release_list = [
#     (1,"har","123")
# ]


# # create database table and populate it with release_list
# table = """ create table users (
#     id integer primary key autoincrement,
#     username text not null,
#     password text not null
# ); """
# cursor.execute("DROP TABLE IF EXISTS users")
# cursor.execute(table )
# cursor.executemany("insert into users values (?,?,?)", release_list)
# # save changes immediatley
# connection.commit()
#connection = sqlite3.connect("login.db")
table = """create table login(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email text not null,
    password text not null); """
release_list = [(1,"xyz@gmail.com","123")]
cursor.execute("DROP TABLE IF EXISTS login")
cursor.execute(table )
cursor.executemany("insert into login values (?,?,?)", release_list)
connection.commit()
table = """create table dairy(
    diary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email text not null,
    Text text ,
    FOREIGN KEY (email)  
    REFERENCES login(email)  
    ); """
release_list = [(1,"xyz@gmail.com","I'm not sad")]
cursor.execute("DROP TABLE IF EXISTS dairy")
cursor.execute(table )
cursor.executemany("insert into dairy values (?,?,?)", release_list)
connection.commit()
table = """CREATE TRIGGER insert_dairy After INSERT  ON login 
  BEGIN
    INSERT INTO dairy(email,text) VALUES(new.email,"") ;
  END; """
cursor.execute(table )
connection.commit()
table = """CREATE TRIGGER delete_dairy After delete  ON login 
  BEGIN
    DELETE FROM dairy WHERE email =old.email ;
  END; """
cursor.execute(table )
connection.commit()


