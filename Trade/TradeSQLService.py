import sqlite3
import sys

class TradeSQLService:

    hasCreatedTradeTable = False

    def createConnection(self, databaseName):
        conn = None
        try:
            conn = sqlite3.connect(databaseName)
        except Error as e:
            print(e)
        return conn
        
    def createAggTradeTable(self, conn):
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
            c = conn.cursor()
            c.execute(CREATE_CACHE_TABLE)
        except:
            print("Failed to create table:", sys.exc_info()[0])
            
    def getTrades(self, conn, limit):
        sql = 'SELECT * FROM aggTrades ORDER BY eventTime ASC'
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            return c.fetchall()
        except BaseException as e:
            print("Failed to get trades", e)
            return None
            
    def getRowCount(self, conn):
        sql = 'SELECT Count(*) FROM aggTrades'
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            return c.fetchall()
        except:
            print("Failed to get row count")
            return None
            
    def getTables(self, conn):
        sql = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
        try:
            c = conn.cursor()
            c.execute(sql)
            conn.commit()
            return c.fetchall()
        except BaseException as e:
            print("Failed to get tables", e)
            return None

