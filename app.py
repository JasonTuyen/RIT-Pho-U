from datetime import datetime
from flask import Flask, render_template, request
import sqlite3
import uuid
import smtplib 

app = Flask(__name__)

con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS inventory (id INTEGER, product TEXT, amount INTEGER, unit TEXT, restock INTEGER)")
cur.close()

#Return the timestamp in which we last checked inventory
def getLastChecked():
    con = sqlite3.connect('timestamp.db')
    cur = con.cursor()
    cur.execute('SELECT time FROM checked ORDER BY time DESC LIMIT 1')
    result = cur.fetchone()
    time = result[0]
    con.close()
    return time

#Homepage
@app.route('/')
def home():
    today = datetime.today()
    formatted_date = today.strftime("%A, %B %d")
    return render_template('index.html', today=formatted_date)

#Read all items in Database
@app.route('/inventory')
def list():
    time = getLastChecked()
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM inventory")
    rows = cur.fetchall(); 
    return render_template("inventory.html",rows = rows, time=time)

#Update an item in Database
@app.route('/inventory', methods=['POST'])
def edit():
    id = request.form['id']
    product = request.form['product']
    amount = request.form['amount']
    unit = request.form['unit']
    restock = request.form['restock']
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("UPDATE inventory SET product=?, amount=?, unit=?, restock=? WHERE id=?", (product.lower(), amount, unit.lower(), restock, id))
    con.commit()
    return list()

#Page to add new item to Database
@app.route('/add')
def addPage():
    return render_template('add.html')

#Function to add new item to Database
@app.route('/add', methods=['POST'])
def addFunc():
    id = str(uuid.uuid4())
    product = request.form['product']
    amount = request.form['amount']
    unit = request.form['unit']
    restock = request.form['restock']
    if not product or not amount or not unit or not restock:
        message = "Error: Please fill all text fields."
        return render_template('message.html', message = message)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO inventory VALUES(?, ?, ?, ?, ?)", (id, product.lower(), amount, unit.lower(), restock))
    con.commit()
    message = "Item sucessfully added."
    return render_template('message.html', message = message)

#Page to delete item(s) from Database
@app.route('/delete')
def deletePage():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from inventory")
    rows = cur.fetchall(); 
    return render_template("delete.html",rows = rows)

#Function to delete item(s) from Database
@app.route('/delete', methods=['POST'])
def deleteFunc():
    product_ids = request.form.getlist('delete[]')
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    for product_id in product_ids:
        cur.execute('DELETE FROM inventory WHERE id = ?', (product_id,))
    con.commit()
    con.close()
    message = "Item sucessfully deleted."
    return render_template('message.html', message = message)

#Complete Check button that saves timestamp of our current check
@app.route('/checked')
def check():
    con = sqlite3.connect("timestamp.db")
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS checked (time TEXT)')
    timestamp = datetime.now().strftime('%A, %m-%d-%Y %H:%M')
    cur.execute('INSERT INTO checked (time) VALUES (?)', (timestamp,))
    message = "Check complete at " + timestamp
    con.commit()
    return render_template('message.html', message = message)

#Send reminder button to send email with low items
@app.route('/reminder')
def reminder():
    try: 
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT product, amount, restock FROM inventory WHERE amount <= restock")
        body = cur.fetchall()
        con.close()
        smtp = smtplib.SMTP('smtp.gmail.com', 587) 
        smtp.starttls() 
        #User Authentication, Must be App Password, see Stackoverflow: https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j
        smtp.login("sender_email_id","sender_email_id_password")
        smtp.sendmail("sender_email_id", "receiver_email_id",body) 
        smtp.quit() 
        message = "Email sent successfully!"
        return render_template('message.html', message = message)
    except Exception as ex: 
        message = "Error sending, try later"
        return render_template('message.html', message = message)