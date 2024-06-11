<?php
$host = "localhost";
$username = "root";
$password = "";
$database = "news_agency";

// Create connection
$conn = mysqli_connect($host, $username, $password, $database);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

$customer_id = mysqli_real_escape_string($conn, $_POST['customer_id']);
$name = mysqli_real_escape_string($conn, $_POST['name']);
$email = mysqli_real_escape_string($conn, $_POST['email']);
$rating = mysqli_real_escape_string($conn, $_POST['rating']);
$comments = mysqli_real_escape_string($conn, $_POST['comments']);

$sql = "INSERT INTO feedback (customer_id, name, email, rating, comments) 
        VALUES ('$customer_id', '$name', '$email', '$rating', '$comments')";

if (mysqli_query($conn, $sql)) {
    echo "New feedback recorded successfully";
} else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}

mysqli_close($conn);
?>
