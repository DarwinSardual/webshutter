import sqlite3 as lite

class SqliteDbConn:

    __connection = None

    @staticmethod
    def createDb():
        sql = """CREATE TABLE IF NOT EXISTS 'urls' (
			'id'	INTEGER PRIMARY KEY AUTOINCREMENT,
			'url'	TEXT,
			'status'	INTEGER,
			'status_label' TEXT,
			'is_checked'	INTEGER
		)"""


    @staticmethod
    def getConnection():
        if not __connection:
            try:
    			__connection = lite.connect('webshutter.db')
    		except:
    			print("Db connection error : ")
    			raise

        return __connection
