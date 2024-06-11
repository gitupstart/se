from flask import Flask, request, jsonify, render_template_string
import mysql.connector
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# MySQL database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="four"
        )
        return connection
    except mysql.connector.Error as err:
        app.logger.error(f"Error connecting to the database: {err}")
        return None

db = get_db_connection()

@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Book Search</title>
    </head>
    <body>
        <h1>Book Search</h1>
        <form action="/search" method="GET">
         <label for="b_id">Enter book id:</label>
        <input type="text" id="b_id" name="b_id"><br>
            <label for="title">Enter book title:</label>
            <input type="text" id="title" name="title"><br>
            <button type="submit">Search</button>
        </form>
        <div id="results"></div>

        <script>
            document.querySelector('form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const title = document.getElementById('title').value;
                const response = await fetch(`/search?title=${title}`);
                const data = await response.json();
                displayResults(data);
            });

            function displayResults(books) {
                const resultsDiv = document.getElementById('results');
                resultsDiv.innerHTML = '';

                if (books.message) {
                    resultsDiv.innerHTML = books.message;
                    return;
                }

                books.forEach(book => {
                    const bookInfo = `<p>Title: ${book.title}, Author: ${book.author}, Rack Number: ${book.rack_number}, Copies Available: ${book.copies_available}</p>`;
                    resultsDiv.innerHTML += bookInfo;
                });
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/search', methods=['GET'])
def search_book():
    db = get_db_connection()
    if db is None:
        return jsonify({"message": "Database connection failed"}), 500

    try:
        title = request.args.get('title')
        if not title:
            return jsonify({"message": "Title parameter is missing"}), 400

        cursor = db.cursor()
        query = "SELECT * FROM books WHERE title LIKE %s"
        cursor.execute(query, ("%" + title + "%",))
        books = cursor.fetchall()
        cursor.close()
        db.close()

        if len(books) == 0:
            return jsonify({"message": "Book not found"}), 404

        results = []
        for book in books:
            result = {
                "title": book[1],
                "author": book[2],
                "rack_number": book[3],
                "copies_available": book[4]
            }
            results.append(result)

        return jsonify(results)

    except mysql.connector.Error as err:
        app.logger.error(f"Database error: {err}")
        return jsonify({"message": "An error occurred", "error": str(err)}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@app.teardown_appcontext
def close_db_connection(exception=None):
    if db:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
