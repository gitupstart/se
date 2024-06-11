from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bookshop_db"
)

# Create a cursor object
cursor = db.cursor()

# Create the books_request table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS books_request (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    request_count INT DEFAULT 1
)
""")

db.commit()

@app.route('/')
def index():
    return render_template('request_form.html')

@app.route('/request_book', methods=['POST'])
def request_book():
    try:
        title = request.form['title']
        author = request.form['author']
        email = request.form.get('email')  # Use get to avoid KeyError if email is not provided

        cursor.execute("""
        INSERT INTO books_request (title, author, email)
        VALUES (%s, %s, %s)
        """, (title, author, email))

        db.commit()
        flash('Book request submitted successfully!', 'success')
    except KeyError as e:
        flash(f'Missing form data: {e}', 'danger')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
