<!-- welcome.php -->
<?php
session_start();
if(!isset($_SESSION['authenticated'])) {
    header("Location: login.php");
    exit(0);
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Welcome</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .btn {
            background-color: #007bff;
            color: #fff;
            border: none;
            padding: 10px;
            cursor: pointer;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome, <?php echo $_SESSION['user']['fname']; ?>!</h2>
        <p>You are now logged in.</p>
        <form action="logout.php" method="POST">
            <button type="submit" name="logout_btn" class="btn">Logout</button>
        </form>
    </div>
</body>
</html>
