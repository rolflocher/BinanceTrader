import sys

class AKlineSQLService:
    def createConnection(self, database):
        self.conn = None
        try:
            self.conn = sqlite3.connect(database)
        except Error as e:
            print(e)

    def createTable(self, table, keys):
        statement = '''CREATE TABLE IF NOT EXISTS klines (
            open real
            high real
            low real
            close real
            volume integer
            time real ASC
            id PRIMARY KEY
        )'''
        try:
            c = conn.cursor()
            c.execute(CREATE_CACHE_TABLE)
        except:
            print("Failed to create table:", sys.exc_info()[0])
            
    def insertKlines(self, klines):
        for kline in klines:
            self.insertKline(kline)
            
    def insertKline(self, kline):
        statement = ''' INSERT OR REPLACE INTO klines(open,high,low,close,volume,time,id)
        VALUES(?,?,?,?,?,?,?) '''
        try:
            cur = conn.cursor()
            cur.execute(statement, kline)
        except:
            print("failed to insert", sys.exc_info()[0])

    def getKlines(self):
                    statement = 'SELECT * FROM klines ORDER BY time ASC'
        try:
            c = conn.cursor()
            c.execute(statement)
            conn.commit()
            return c.fetchall()
        except:
            print("Failed to get trades")
            return None
