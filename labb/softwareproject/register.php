 <!-- register.php -->
<?php session_start(); ?>
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Register System in PHP MySQL</title>
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
            width: 300px;
        }
        h2 {
            text-align: center;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
        }
        .form-group input {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        .btn {
            background-color: #007bff;
            color: #fff;
            border: none;
            padding: 10px;
            width: 100%;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        .alert {
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
            text-align: center;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
        }
        .alert-warning {
            background-color: #fff3cd;
            color: #856404;
        }
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Register</h2>
        <?php
        if(isset($_SESSION['message'])) {
            echo '<div class="alert alert-warning">'.$_SESSION['message'].'</div>';
            unset($_SESSION['message']);
        }
        ?>
        <form action="registercode.php" method="POST">
            <div class="form-group">
                <label>First Name</label>
                <input type="text" name="fname" required>
            </div>
            <div class="form-group">
                <label>Last Name</label>
                <input type="text" name="lname" required>
            </div>
            <div class="form-group">
                <label>Email Id</label>
                <input type="email" name="email" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" required>
            </div>
            <div class="form-group">
                <label>Confirm Password</label>
                <input type="password" name="confirm_password" required>
            </div>
            <button type="submit" name="register_btn" class="btn">Register</button>
        </form>
    </div>
</body>
</html>
