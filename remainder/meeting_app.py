from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import threading

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.urandom(24)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'meeting_db'

mysql = MySQL(app)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/schedule_meeting', methods=['GET', 'POST'])
def schedule_meeting():
    msg = ''
    if request.method == 'POST' and 'title' in request.form and 'date_time' in request.form and 'email' in request.form:
        title = request.form['title']
        description = request.form.get('description', '')
        date_time = request.form['date_time']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO meetings (title, description, date_time, email) VALUES (%s, %s, %s, %s)', (title, description, date_time, email))
        mysql.connection.commit()
        msg = 'Meeting scheduled successfully!'
        schedule_reminder(title, description, date_time, email)
    return render_template('schedule_meeting.html', msg=msg)

@app.route('/meetings')
def meetings():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM meetings ORDER BY date_time ASC')
    meetings = cursor.fetchall()
    return render_template('meetings.html', meetings=meetings)

def schedule_reminder(title, description, date_time, email):
    reminder_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M') - timedelta(minutes=30)  # Reminder 30 minutes before the meeting
    delay = (reminder_time - datetime.now()).total_seconds()
    threading.Timer(delay, send_reminder, args=[title, description, date_time, email]).start()

def send_reminder(title, description, date_time, email):
    msg = Message('Meeting Reminder', sender='your_email@gmail.com', recipients=[email])
    msg.body = f'Reminder: You have a meeting scheduled.\n\nTitle: {title}\nDescription: {description}\nDate & Time: {date_time}'
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
