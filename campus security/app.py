from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db_config = {
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': '127.0.0.1',
    'database': 'security_management',
    'raise_on_warnings': True
}

# Database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return None

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    identity_number = request.form['identity_number']
    password = request.form['password']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE identity_number = %s AND password = %s", (identity_number, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        session['user_id'] = user['id']
        session['role'] = user['role']
        if user['role'] == 'manager':
            return redirect(url_for('manager_dashboard'))
        else:
            return redirect(url_for('security_dashboard'))
    else:
        return "Invalid credentials"

@app.route('/manager_dashboard')
def manager_dashboard():
    if 'role' in session and session['role'] == 'manager':
        return render_template('manager_dashboard.html')
    else:
        return redirect(url_for('index'))

@app.route('/create_routine', methods=['GET', 'POST'])
def create_routine():
    if 'role' in session and session['role'] == 'manager':
        if request.method == 'POST':
            security_id = request.form['security_id']
            place_id = request.form['place_id']
            duty_date = request.form['duty_date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO routines (security_id, place_id, duty_date, start_time, end_time) VALUES (%s, %s, %s, %s, %s)",
                           (security_id, place_id, duty_date, start_time, end_time))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('manager_dashboard'))
        else:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE role='security'")
            security_persons = cursor.fetchall()
            cursor.execute("SELECT * FROM places")
            places = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('create_routine.html', security_persons=security_persons, places=places)
    else:
        return redirect(url_for('index'))

@app.route('/approve_leave', methods=['GET', 'POST'])
def approve_leave():
    if 'role' in session and session['role'] == 'manager':
        if request.method == 'POST':
            leave_id = request.form['leave_id']
            status = request.form['status']
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE leave_requests SET status = %s WHERE id = %s", (status, leave_id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('manager_dashboard'))
        else:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT lr.id, u.name, lr.request_date, lr.status FROM leave_requests lr JOIN users u ON lr.security_id = u.id WHERE lr.status = 'pending'")
            leave_requests = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('approve_leave.html', leave_requests=leave_requests)
    else:
        return redirect(url_for('index'))

@app.route('/view_status')
def view_status():
    if 'role' in session and session['role'] == 'manager':
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT u.id, u.name, (SELECT COUNT(*) FROM leave_requests lr WHERE lr.security_id = u.id AND lr.status = 'approved') AS leaves_taken FROM users u WHERE u.role = 'security'")
        security_status = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('view_status.html', security_status=security_status)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
