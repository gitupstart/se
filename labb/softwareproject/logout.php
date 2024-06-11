<!-- logout.php -->
<?php
session_start();
if(isset($_POST['logout_btn'])) {
    session_destroy();
    unset($_SESSION['authenticated']);
    unset($_SESSION['user']);
    header("Location: login.php");
    exit(0);
}
?>
