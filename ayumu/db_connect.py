# https://proglib.io/p/kak-podruzhit-python-i-bazy-dannyh-sql-podrobnoe-rukovodstvo-2020-02-27/amp/
import sqlite3
from sqlite3 import Error


""" ПОДКЛЮЧЕНИЕ К БД """
def create_connection(path):
	connection = None
	try:
		connection = sqlite3.connect(path)
		print("Connection SQLite DB successful.")
	except Error as e:
		print(f"The error '{e}' occurred.")

	return connection

# создаем соединение с БД
connection = create_connection("db.sqlite3")

""" СОЗДАНИЕ ТАБЛИЦ """
def execute_query(connection, query):
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		connection.commit()
		print("Query executed successfully.")
	except Error as e:
		print(f"The error '{e}' occurred.")




""" ИЗВЛЕЧЕНИЕ ИЗ ТАБЛИЦ """
def execute_read_query(connection, query):
	cursor = connection.cursor()
	result = None
	try:
		cursor.execute(query)
		result = cursor.fetchall()
		return result
	except Error as e:
		print(f"The error '{e}' occurred.")

