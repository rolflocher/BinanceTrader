
import sqlite3
import asyncio
import websockets
import json
import time
import sys

baseEndpoint = "wss://fstream.binance.com"

rowQueue = []

def createConnection():
    conn = None
    try:
        conn = sqlite3.connect('aggTrades.db')
    except Error as e:
        print(e)
    return conn

def createAggTradeTable(conn):
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

def insertAggTrade(conn, aggTrade):
    sql = ''' INSERT OR REPLACE INTO aggTrades(price,quantity,buyerMarkerMaker,tradeTime,eventTime,aggTradeId)
    VALUES(?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, aggTrade)
    except:
        print("failed to insert", sys.exc_info()[0])
        
def process_message(msg):
    msg = json.loads(msg)
    marketMaker = 0 if msg["m"] == False else 1
    aggTrade = (float(msg['p']), float(msg['q']), marketMaker, msg['T'], msg['E'], msg['a'])
    rowQueue.append(aggTrade)

async def watchAggregateTrades(symbol):
    uri = baseEndpoint + "/ws/" + "btcusdt@trade"
    async with websockets.connect(uri) as websocket:
        lastPong = time.time()
        while True:
            subcriptionResponse = await websocket.recv()
            process_message(subcriptionResponse)
            currentTime = time.time()
            if currentTime - lastPong > 60:
                await websocket.pong()
                lastPong = currentTime

def writeRows():
    conn = createConnection()
    with conn:
        createAggTradeTable(conn)
        while rowQueue:
            row = rowQueue.pop(0)
            insertAggTrade(conn, row)
            print("writing", row)
        conn.commit()

async def writeRowLoop():
    while True:
        await asyncio.sleep(20)
        writeRows()

loop = asyncio.get_event_loop()
tradeTask = loop.create_task(watchAggregateTrades("btcusdt"))
saveTask = loop.create_task(writeRowLoop())

loop.run_forever()
