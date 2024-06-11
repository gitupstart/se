from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="rrts_db"
)

# Create a cursor object
cursor = db.cursor()

# Create the repair_requests table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS repair_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    road_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending'
)
""")

db.commit()

@app.route('/')
def index():
    return render_template('issue_form.html')

@app.route('/raise_issue', methods=['POST'])
def raise_issue():
    try:
        name = request.form['name']
        address = request.form['address']
        email = request.form.get('email')
        phone = request.form.get('phone')
        road_name = request.form['road_name']
        description = request.form['description']

        cursor.execute("""
        INSERT INTO repair_requests (name, address, email, phone, road_name, description)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, address, email, phone, road_name, description))

        db.commit()
        flash('Repair request submitted successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
