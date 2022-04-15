import sqlite3
import pandas as pd 
import csv

con = sqlite3.connect('database.db')
cursor = con.cursor()

def createTableUsers():
	cursor.execute('''
		CREATE TABLE if not exists users(
		firstName varchar(256),
		lastName varchar(256),
		age integer,
		salary integer,
		start_dttm datetime default current_timestamp,
		effective_from_dttm datetime default current_timestamp,
		end_dttm datetime default (datetime('2999-12-31 23:59:59')),
		deleted_flg integer default 0
	);

	''')

def add_user(firstName, lastName, age, salary):
	cursor.execute('''
		INSERT INTO users (firstName, lastName, age, salary) VALUES (?, ?, ?, ?);
	''', [firstName, lastName, age, salary])
	con.commit()

def update_user(firstName, lastName, age, salary):
	cursor.execute('''
		update users
		set	end_dttm = current_timestamp
		where firstName = ? and lastName = ?
	''', [firstName, lastName])
	cursor.execute('''
		INSERT INTO users (firstName, lastName, age, salary) VALUES (?, ?, ?, ?)
	''', [firstName, lastName, age, salary])
	con.commit()

def add_or_update(firstName, lastName, age, salary):
	cursor.execute('select * from users where firstName = ? and lastName = ?', [firstName, lastName])
	if cursor.fetchone is None:
		add_user(firstName, lastName, age, salary)
	else:
		update_user(firstName, lastName, age, salary) 

def deleteUser(firstName, lastName):
	cursor.execute('''
		update users
		set deleted_flg = 1
		where firstName = ? and lastName = ?
	''', [firstName, lastName])
	con.commit()

def saveTable(table, path, date):
	with open(path, mode = 'w', encoding = 'UTF-8') as w_file:
		file_writer = csv.writer(w_file, delimiter = ',')
		cursor.execute(f'select * from {table} where {date} between effective_from_dttm and end_dttm')
		for row in cursor.fetchall():
			print(row)
			file_writer.writerow(row)

createTableUsers()
add_user('John', 'Smith', 35, 9000)
add_user('Mark', 'Durie', 47, 10000)
add_user('John', 'Smith', 80, 7500)
deleteUser('John', 'Smith')
add_or_update('John', 'Down', 80, 7500)
#saveTable('users', 'C://Users//Федор//Documents//Python Scripts//1.csv', 'current_timestamp') 
cursor.execute('select * from users')
for row in cursor.fetchall():
	print(row)
df.to_csv(database.db, sep = '\t')