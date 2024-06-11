from werkzeug.security import generate_password_hash
import mysql.connector

username = 'root'
password = ''
email = 'abc@gmail.com'
password_hash = generate_password_hash(password)

conn = mysql.connector.connect(user='root', password='', host='localhost', database='AdminDB')
cursor = conn.cursor()
cursor.execute("INSERT INTO Admins (username, password_hash, email) VALUES (%s, %s, %s)", (username, password_hash, email))
conn.commit()
cursor.close()
conn.close()
print("Admin user created successfully.")
