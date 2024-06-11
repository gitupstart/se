<?php
$host = "localhost";
$username = "root";
$password = "";
$database = "book";

// Create connection
$conn = mysqli_connect($host, $username, $password, $database);
// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Sanitize and validate input data
$customer_name = mysqli_real_escape_string($conn, $_POST['name']);
$email = mysqli_real_escape_string($conn, $_POST['email']);
$book_title = mysqli_real_escape_string($conn, $_POST['book_title']);
$author_name = mysqli_real_escape_string($conn, $_POST['author_name']);

$sql = "INSERT INTO book_requests (customer_name, email, book_title, author_name) 
        VALUES ('$customer_name', '$email', '$book_title', '$author_name')";

if (mysqli_query($conn, $sql)) {
    echo "Request submitted successfully";
} else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}
mysqli_close($conn);
?>
