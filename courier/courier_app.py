from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.urandom(24)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'courier_db'

mysql = MySQL(app)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_courier', methods=['GET', 'POST'])
def add_courier():
    msg = ''
    if request.method == 'POST' and 'sender_name' in request.form and 'receiver_name' in request.form and 'status' in request.form:
        sender_name = request.form['sender_name']
        receiver_name = request.form['receiver_name']
        status = request.form['status']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO couriers (sender_name, receiver_name, status) VALUES (%s, %s, %s)', (sender_name, receiver_name, status))
        mysql.connection.commit()
        msg = 'Courier added successfully!'
    return render_template('add_courier.html', msg=msg)

@app.route('/courier_status', methods=['GET', 'POST'])
def courier_status():
    if request.method == 'POST' and 'courier_id' in request.form:
        courier_id = request.form['courier_id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM couriers WHERE id = %s', (courier_id,))
        courier = cursor.fetchone()
        if courier:
            return render_template('courier_status.html', courier=courier)
        else:
            return 'Courier not found!'
    return render_template('check_status.html')

if __name__ == '__main__':
    app.run(debug=True)
