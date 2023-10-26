import sqlite3
import uuid

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