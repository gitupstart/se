<!-- registercode.php -->
<?php
session_start();
include('dbconfig.php');

if(isset($_POST['register_btn'])) {
    $fname = mysqli_real_escape_string($conn, $_POST['fname']);
    $lname = mysqli_real_escape_string($conn, $_POST['lname']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);
    $confirm_password = mysqli_real_escape_string($conn, $_POST['confirm_password']);

    if($password == $confirm_password) {
        // Check Email
        $checkemail = "SELECT email FROM users WHERE email='$email' LIMIT 1";
        $checkemail_run = mysqli_query($conn, $checkemail);

        if(mysqli_num_rows($checkemail_run) > 0) {
            // Email already exists
            $_SESSION['message'] = "Email already exists";
            header("Location: register.php");
            exit(0);
        } else {
            // No password hashing
            $user_query = "INSERT INTO users (fname, lname, email, password) VALUES ('$fname', '$lname', '$email', '$password')";
            $user_query_run = mysqli_query($conn, $user_query);

            if($user_query_run) {
                $_SESSION['message'] = "Registered successfully";
                header("Location: login.php");
                exit(0);
            } else {
                $_SESSION['message'] = "Something went wrong!";
                header("Location: register.php");
                exit(0);
            }
        }
    } else {
        $_SESSION['message'] = "Password and confirm password do not match";
        header("Location: register.php");
        exit(0);
    }
}
?>
