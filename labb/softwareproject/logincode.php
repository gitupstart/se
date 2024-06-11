<!-- logincode.php -->
<?php
session_start();
include('dbconfig.php');

if(isset($_POST['login_btn'])) {
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);
    
    $query = "SELECT * FROM users WHERE email='$email' LIMIT 1";
    $query_run = mysqli_query($conn, $query);

    if(mysqli_num_rows($query_run) > 0) {
        $user = mysqli_fetch_assoc($query_run);
        // No password verification
        if($password == $user['password']) {
            $_SESSION['authenticated'] = true;
            $_SESSION['user'] = $user;
            header("Location: welcome.php");
            exit(0);
        } else {
            $_SESSION['message'] = "Invalid password";
            header("Location: login.php");
            exit(0);
        }
    } else {
        $_SESSION['message'] = "No user found with this email";
        header("Location: login.php");
        exit(0);
    }
}
?>
