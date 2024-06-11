<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "time_manag";

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Query to fetch executives and their meeting times
$sql = "SELECT * FROM executives";
$result = mysqli_query($conn, $sql);

if (mysqli_num_rows($result) > 0) {
    echo "<h1>Executive Meeting Time Dashboard</h1>";
    
    // Display each executive's meeting times
    while ($row = mysqli_fetch_assoc($result)) {
        // Sum of meeting times for the week
        $totalMeetingTime = array_sum(array_slice($row, 2)); 
        echo "<h3>" . htmlspecialchars($row['name']) . "</h3>";
        echo "<p>Total Meeting Time in a week: " . $totalMeetingTime . " hours</p>";
    }
} else {
    echo "No executives found.";
}

mysqli_close($conn);
?>
