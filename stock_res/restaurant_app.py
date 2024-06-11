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
app.config['MYSQL_DB'] = 'restaurant_db'

mysql = MySQL(app)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    msg = ''
    if request.method == 'POST' and 'item_name' in request.form and 'quantity' in request.form:
        item_name = request.form['item_name']
        quantity = int(request.form['quantity'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO stock (item_name, quantity) VALUES (%s, %s)', (item_name, quantity))
        mysql.connection.commit()
        msg = 'Item added successfully!'
    return render_template('add_item.html', msg=msg)


@app.route('/check_stock', methods=['GET', 'POST'])
def check_stock():
    if request.method == 'POST' and 'item_name' in request.form:
        item_name = request.form['item_name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM stock WHERE item_name = %s', (item_name,))
        item = cursor.fetchone()
        if item:
            return render_template('stock_status.html', item=item)
        else:
            return 'Item not found!'
    return render_template('check_stock.html')

if __name__ == '__main__':
    app.run(debug=True)
