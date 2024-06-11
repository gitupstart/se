from werkzeug.security import check_password_hash

# The hashed password retrieved from the database
stored_hash = 'scrypt:32768:8:1$gZ5Ns0XqpmaKuzND$1ab089779d1c95bddf0930cd882c30bb2dd4dc579a923ddd529b3c833b689bed39'

# Plain text password (empty string)
password = ''

# Verify the password
if check_password_hash(stored_hash, password):
    print("Password is correct.")
else:
    print("Password is incorrect.")
