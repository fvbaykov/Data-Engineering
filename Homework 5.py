import sqlite3
import json
connect = sqlite3.connect('database.db')
cursor = connect.cursor()
def create_table(): 
	cursor.execute(''' 
		CREATE TABLE if not exists client(
		name varchar(128),
		lastname varchar(128),
		age integer
		)
	''')


def insert_new_client(name, lastname, age):
	cursor.execute('''
	INSERT INTO client (name, lastname, age) VALUES (?, ?, ?)
	''', [name, lastname, age])
	connect.commit()

def avg_age():
	cursor.execute('''
		SELECT avg(age) from client
	''')
	for row in cursor.fetchall():
		print(row)

def insert_client(sourse):
	with open(sourse) as json_file:
		data = json.load(json_file)
		for p in data: 
			cursor.execute(''' 
				INSERT INTO client (name, lastname, age) VALUES (?, ?, ?)
			''', [p['name'], p['lastname'], p['age']])

create_table()
insert_client('1.json')
avg_age()