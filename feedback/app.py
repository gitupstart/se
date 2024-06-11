from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
db = SQLAlchemy(app)
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    address=db.Column(db.String(100), nullable=False)



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'feedback_db'

mysql = MySQL(app)


@app.route('/')
def feedback_form():
    return render_template('feedback_form')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    feedback_text = request.form['feedback']
    address=request.form['address']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO feedback (name, email, feedback,address) VALUES (%s, %s, %s,%s)", (name, email, feedback_text,address))
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return 'Thank you for your feedback!'
if __name__ == '__main__':
    app.run(debug=True)
