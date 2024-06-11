<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "road_repair";

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Escape user inputs for security
$resident_name = mysqli_real_escape_string($conn, $_POST['resident_name']);
$contact_number = mysqli_real_escape_string($conn, $_POST['contact_number']);
$suburb = mysqli_real_escape_string($conn, $_POST['suburb']);
$road_name = mysqli_real_escape_string($conn, $_POST['road_name']);
$issue_description = mysqli_real_escape_string($conn, $_POST['issue_description']);

// Insert data into repair_requests table
$sql = "INSERT INTO repair_requests (resident_name, contact_number, suburb, road_name, issue_description)
        VALUES ('$resident_name', '$contact_number', '$suburb', '$road_name', '$issue_description')";

if (mysqli_query($conn, $sql)) {
    echo "Request submitted successfully";
} else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}

mysqli_close($conn);
?>
