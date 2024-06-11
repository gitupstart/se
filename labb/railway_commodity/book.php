<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "railway_commodity";

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Escape user inputs for security
$customer_name = mysqli_real_escape_string($conn, $_POST['customer_name']);
$contact_number = mysqli_real_escape_string($conn, $_POST['contact_number']);
$schedule_id = mysqli_real_escape_string($conn, $_POST['schedule_id']);
$quantity = mysqli_real_escape_string($conn, $_POST['quantity']);

// Insert data into bookings table
$sql = "INSERT INTO bookings (schedule_id, customer_name, contact_number, quantity) VALUES ('$schedule_id', '$customer_name', '$contact_number', '$quantity')";

if (mysqli_query($conn, $sql)) {
    echo "Booking confirmed successfully";
} else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}

mysqli_close($conn);
?>
