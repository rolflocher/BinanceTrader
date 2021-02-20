import sqlite3
import sys

class SQLService:
    
    conn = None
    hasCreatedTradeTable = False
    hasCreatedBookTable = False

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
            
    def getTrades(self, limit = None):
        sql = 'SELECT * FROM aggTrades ORDER BY eventTime ASC'
        if not limit == None:
            sql = sql + ' LIMIT ' + str(int(limit))
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
            return c.fetchall()
        except:
            print("Failed to get trades")
            return None
            
    def getRowCount(self):
        sql = 'SELECT Count(*) FROM aggTrades'
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
            return c.fetchall()
        except:
            print("Failed to get row count")
            return None

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
