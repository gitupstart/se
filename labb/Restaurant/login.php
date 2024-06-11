<?php
$servername = "localhost";
$dbusername = "root";
$dbpassword = "";
$dbname = "restaurant";

// Create connection
$conn = mysqli_connect($servername, $dbusername, $dbpassword, $dbname);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Retrieve entered username and password from form
$username = mysqli_real_escape_string($conn, $_POST['username']);
$password = mysqli_real_escape_string($conn, $_POST['password']);

// Query to check credentials
$sql = "SELECT * FROM managers WHERE username='$username' AND password='$password'";
$result = mysqli_query($conn, $sql);

// Check if credentials match
if (mysqli_num_rows($result) == 1) {
    // Redirect to prices.php on successful login
    header("Location: prices.php");
    exit();
} else {
    // Redirect back to index.php with error message on failed login
    header("Location: index.php?error=1");
    exit();
}

mysqli_close($conn);
?>
