import sqlite3
import sys

class SQLService:
	
	conn = None
	hasCreatedTradeTable = False
	hasCreatedBookTable = False
	existingTables = {}

	def createConnection(self, databaseName):
		try:
			self.conn = sqlite3.connect(databaseName)
		except Error as e:
			print(e)
		return self.conn
		
	def createAggTradeTable(self):
		if self.hasCreatedTradeTable:
			return
		self.hasCreatedTradeTable = True
		CREATE_CACHE_TABLE = '''CREATE TABLE IF NOT EXISTS aggTrades (
			price real,
			quantity real,
			buyerMarkerMaker integer,
			tradeTime integer,
			eventTime integer ASC,
			aggTradeId PRIMARY KEY
		  )'''
		try:
			c = self.conn.cursor()
			c.execute(CREATE_CACHE_TABLE)
		except:
			print("Failed to create table:", sys.exc_info()[0])
			
	def insertAggTrade(self, aggTrade):
		sql = ''' INSERT OR REPLACE INTO aggTrades(price,quantity,buyerMarkerMaker,tradeTime,eventTime,aggTradeId)
		VALUES(?,?,?,?,?,?) '''
		try:
			cur = self.conn.cursor()
			cur.execute(sql, aggTrade)
		except:
			print("failed to insert", sys.exc_info()[0])

	def createBookTable(self):
		if self.hasCreatedBookTable:
			return
		self.hasCreatedBookTable = True
		CREATE_CACHE_TABLE = '''CREATE TABLE IF NOT EXISTS depthDiffs (
			time integer,
			firstId integer,
			finalId PRIMARY KEY,
			bids text,
			asks text
		  )'''
		try:
			c = self.conn.cursor()
			c.execute(CREATE_CACHE_TABLE)
		except:
			print("Failed to create table:", sys.exc_info()[0])
			
	def insertBookDiff(self, diff):
		sql = ''' INSERT OR REPLACE INTO depthDiffs(time,firstId,finalId,bids,asks)
		VALUES(?,?,?,?,?) '''
		try:
			cur = self.conn.cursor()
			cur.execute(sql, diff)
		except:
			print("failed to insert", sys.exc_info()[0])
			
	def getDepthDiffs(self, limit = None):
		sql = 'SELECT * FROM depthDiffs ORDER BY time ASC'
		if not limit == None:
			sql = sql + ' LIMIT ' + str(int(limit))
		try:
			c = self.conn.cursor()
			c.execute(sql)
			self.conn.commit()
			return c.fetchall()
		except:
			print("Failed to get depth diffs")
			return None

	def createBookSeedTable(self):
		CREATE_CACHE_TABLE = '''CREATE TABLE IF NOT EXISTS depthSeed (
			lastUpdateId PRIMARY KEY,
			bids text,
			asks text
		  )'''
		try:
			c = self.conn.cursor()
			c.execute(CREATE_CACHE_TABLE)
		except:
			print("Failed to create table:", sys.exc_info()[0])
			
	def insertBookSeed(self, seed):
		sql = ''' INSERT OR REPLACE INTO depthSeed(lastUpdateId,bids,asks)
		VALUES(?,?,?) '''
		try:
			cur = self.conn.cursor()
			cur.execute(sql, seed)
		except:
			print("failed to insert", sys.exc_info()[0])
			
	def getBookSeeds(self, limit = None):
		sql = 'SELECT * FROM depthSeed ORDER BY lastUpdateId DESC'
		if not limit == None:
			sql = sql + ' LIMIT ' + str(int(limit))
		try:
			c = self.conn.cursor()
			c.execute(sql)
			self.conn.commit()
			return c.fetchall()
		except:
			print("Failed to get depth diffs")
			return None

	def hasCreatedTable(self, name):
		return name in self.existingTables

	def createTable(self, name):
		if self.hasCreatedTable(name):
			return
		self.existingTables[name] = True
		CREATE_CACHE_TABLE = """CREATE TABLE IF NOT EXISTS {0} (
			time integer,
			lastId PRIMARY KEY,
			bids text,
			asks text
		  )""".format(name)
		try:
			c = self.conn.cursor()
			c.execute(CREATE_CACHE_TABLE)
			self.conn.commit()
		except BaseException as e:
			print("Failed to create", name, "table.", e)

	def insert(self, name, row):
		sql = "INSERT OR REPLACE INTO {0}(".format(name)
		if name == "books":
			sql += "time, lastId, bids, asks"
			sql += ")VALUES(?,?,?,?)"
		try:
			cur = self.conn.cursor()
			cur.execute(sql, row)
			self.conn.commit()
		except BaseException as e:
			print("Failed to insert", name, e)

	def get(self, name, limit = None, after = None):
		sql = "SELECT * FROM {}".format(name)
		index = None
		if name == "aggTrades":
			index = "eventTime"
		else:
			index = "time"
		if not after == None:
			sql += " WHERE {} > {}".format(index, after)
		sql += " ORDER BY {} ASC".format(index)
		if not limit == None:
			sql += " LIMIT {0}".format(str(int(limit)))
		print(sql)
		try:
			c = self.conn.cursor()
			c.execute(sql)
			return c.fetchall()
		except BaseException as e:
			print("Failed to get", name, "rows.", e)
			return None
			
	def drop(self, name):
		sql = "DROP TABLE {}".format(name)
		try:
			cur = self.conn.cursor()
			cur.execute(sql)
			self.conn.commit()
		except BaseException as e:
			print("Failed to drop", name, e)
			
	def getRowCount(self, name):
		sql = "SELECT Count(*) FROM {}".format(name)
		try:
			c = self.conn.cursor()
			c.execute(sql)
			return c.fetchall()
		except BaseException as e:
			print("Failed to get row count for", name, e)
			return None
