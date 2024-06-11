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

// Query to fetch item prices and stock
$sql = "SELECT item_name, price, stock FROM menu_items";
$result = mysqli_query($conn, $sql);

if (mysqli_num_rows($result) > 0) {
    echo "<h2>Item Prices and Stock</h2>";
    echo "<table border='1'>
            <tr>
                <th>Item Name</th>
                <th>Price</th>
                <th>Stock</th>
            </tr>";
    while ($row = mysqli_fetch_assoc($result)) {
        echo "<tr>
                <td>" . $row['item_name'] . "</td>
                <td>" . $row['price'] . "</td>
                <td>" . $row['stock'] . "</td>
              </tr>";
    }
    echo "</table>";
} else {
    echo "No items found.";
}

mysqli_close($conn);
?>
