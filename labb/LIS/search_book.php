<?php
$host = "localhost";
$username = "root";
$password = "";
$database = "library_system";

// Create connection
$conn = mysqli_connect($host, $username, $password, $database);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Check if the form has been submitted and 'isbn' key exists in the $_GET array
if ($_SERVER["REQUEST_METHOD"] == "GET" && isset($_GET['isbn'])) {
    $isbn = mysqli_real_escape_string($conn, $_GET['isbn']);

    // Query to check book availability
    $sql = "SELECT * FROM books WHERE isbn = '$isbn'";
    $result = mysqli_query($conn, $sql);

    if (mysqli_num_rows($result) > 0) {
        $book = mysqli_fetch_assoc($result);


        echo "Book Title: " . $book['title'] . "<br>";
        echo "Author: " . $book['author'] . "<br>";
        echo "Rack Number: " . $book['rack_number'] . "<br>";
        echo "Available Copies: " . $book['copies'] . "<br>";
    } else {
        echo "The book with ISBN $isbn is not available in the library.";
    }
} else {
    echo "Please enter an ISBN to search for a book.";
}

mysqli_close($conn);
?>

<!DOCTYPE html>
<html>
<head>
    <title>Search Book</title>
</head>
<body>
    <h1>Search Book</h1>
    <form method="get" action="search_book.php">
        <label for="isbn">Enter ISBN:</label><br>
        <input type="text" id="isbn" name="isbn" required><br><br>
        <input type="submit" value="Search">
    </form>
</body>
</html>
