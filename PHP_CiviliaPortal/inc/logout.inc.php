<?php
    session_start();
    require_once('../config/config.php');
    if (isset($_POST['submit'])){
        session_unset();
        session_destroy();
        header("Location: ". ROOT_URL);
        exit();
    }
 ?>
