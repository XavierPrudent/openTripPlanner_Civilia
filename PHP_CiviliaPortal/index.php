<meta charset="UTF-8">

<?php
    require('config/config.php');
    require('config/db.php');


    session_start();
    if (isset($_SESSION['user_id'])) {
        header('Location: ' . HOME_LOGGEDIN_URL);
        exit();
    } else {
        header('Location: ' . HOME_NOT_LOGGEDIN_URL);
        exit();
    }

?>
