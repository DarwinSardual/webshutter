import sqlite3 as lite

class SqliteCon():

	def __init__(self):
		self.conn = None
		self.__createDb()

	def connect(self):
		try:
			self.con = lite.connect('webshutter.db')
		except:
			print("Db connection error : ")
			raise

	def __createDb(self):
		sql = """CREATE TABLE IF NOT EXISTS 'urls' (
			'id'	INTEGER PRIMARY KEY AUTOINCREMENT,
			'url'	TEXT,
			'status'	INTEGER,
			'status_label' TEXT,
			'is_checked'	INTEGER
		)"""
		self.execute(sql)

	def close(self):
		if self.con != None:
			self.con.close()

	def execute(self, sql):
		self.connect()
		try:
			cur = self.con.cursor()
			cur.execute(sql)
		except:
			print ("Db query execution error : ")
			raise

		self.close()

	def insert(self, sql, params):
		self.connect()
		try:
			cur = self.con.cursor()
			cur.execute(sql, params)
			self.con.commit()
			id = cur.lastrowid
			self.close()
			return id
		except:
			print("Db query execution error : ")
			raise

		self.close()
		return 0

	def update(self, sql, params):
		self.connect()
		try:
			cur = self.con.cursor()
			cur.execute(sql, params)
			self.con.commit()
		except:
			print("Db query execution error : ")
			raise

		self.close()

	def delete(self, sql, params):
		self.connect()
		try:
			cur = self.con.cursor()
			cur.execute(sql, params)
			self.con.commit()
		except:
			print("Db query execution error : ")
			raise

		self.close()

	def fetchall(self, sql, params = ()):
		self.connect()
		try:
			cur = self.con.cursor()
			cur.execute(sql, params)
			data = cur.fetchall()
			self.close()
			return data
		except:
			print("Db fetch query execution error : ")
			raise
		self.close()
		return None
