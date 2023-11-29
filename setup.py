import sqlite3
import uuid
from datetime import datetime

con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS inventory")
cur.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER, product TEXT, amount INTEGER, unit TEXT, restock INTEGER)")

id = str(uuid.uuid4())
product = "Apple"
amount = 10
unit = 'Boxes'
restock = 5
cur.execute("INSERT INTO inventory VALUES(?, ?, ?, ?, ?)", (id, product, amount, unit, restock))

id = str(uuid.uuid4())
product = "Pies"
amount = 1
unit = 'Boxes'
restock = 5
cur.execute("INSERT INTO inventory VALUES(?, ?, ?, ?, ?)", (id, product, amount, unit, restock))

id = str(uuid.uuid4())
product = "Oranges"
amount = 20
unit = 'Boxes'
restock = 5
cur.execute("INSERT INTO inventory VALUES(?, ?, ?, ?, ?)", (id, product, amount, unit, restock))

con.commit()
cur.close()

con = sqlite3.connect("timestamp.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS checked")
cur.execute('CREATE TABLE IF NOT EXISTS checked (time TEXT)')
timestamp = datetime.now().strftime('%A, %m-%d-%Y %H:%M')
cur.execute('INSERT INTO checked (time) VALUES (?)', (timestamp,))
con.commit()
cur.close()
