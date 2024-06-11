from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="three"
)

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM admins WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('/login', error='Invalid Credentials. Please try again.')
    return render_template('/login')

# Route for the dashboard page (only accessible after login)
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('/dashboard')

# Route to logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
