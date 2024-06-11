from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime
import os

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.urandom(24)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'airline_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/flights', methods=['GET', 'POST'])
def flights():
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM flights WHERE source = %s AND destination = %s', (source, destination))
        flights = cursor.fetchall()
        return render_template('flights.html', flights=flights)
    return render_template('search_flights.html')

@app.route('/book/<int:flight_id>', methods=['POST'])
def book(flight_id):
    if 'loggedin' in session:
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO bookings (user_id, flight_id) VALUES (%s, %s)', (user_id, flight_id))
        mysql.connection.commit()
        return redirect(url_for('view_bookings'))
    return redirect(url_for('login'))

@app.route('/view_bookings')
def view_bookings():
    if 'loggedin' in session:
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT bookings.id, flights.source, flights.destination, flights.departure_time, flights.arrival_time, flights.price FROM bookings JOIN flights ON bookings.flight_id = flights.id WHERE bookings.user_id = %s', (user_id,))
        bookings = cursor.fetchall()
        return render_template('bookings.html', bookings=bookings)
    return redirect(url_for('login'))

@app.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel(booking_id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM bookings WHERE id = %s', (booking_id,))
        mysql.connection.commit()
        return redirect(url_for('view_bookings'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
