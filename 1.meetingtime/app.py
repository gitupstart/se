from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='one'
    )

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT executives.name, 
               SUM(TIMESTAMPDIFF(MINUTE, meetings.start_time, meetings.end_time)) as total_meeting_time 
        FROM executives 
        LEFT JOIN meetings ON executives.id = meetings.executive_id 
        GROUP BY executives.name
    """)
    data = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
