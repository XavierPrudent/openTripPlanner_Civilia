<?php
    session_start();
    require_once('../config/config.php');
    require_once('../config/db.php');

    if (filter_has_var(INPUT_POST, 'submit')){
        $email = mysqli_real_escape_string($conn, $_POST['username']);
        $pwd = mysqli_real_escape_string($conn, $_POST['password']);

        if (empty($email) || empty($pwd)){
            header("Location: ".HOME_NOT_LOGGEDIN_URL);
            exit();
        } else {
            // user can either connect with email or society name
            $query = "SELECT * FROM " . TABLE_USERS_NAME . " WHERE " . TABLE_USERS_EMAIL_COL_NAME . "='$email'";

            $result = mysqli_query($conn, $query);

            $resultCheck = mysqli_num_rows($result);

            if ($resultCheck < 1) {
                //header("Location: ".HOME_NOT_LOGGEDIN_URL."?". LOGIN_STATUS_INURL."=".ERROR_INURL);
                header("Location: ". HOME_NOT_LOGGEDIN_URL);
                exit();
            } else {
                // store one row of the db in a php array
                if ($row = mysqli_fetch_assoc($result)){
                    //De-hasshing password
                    $hashedPwdCheck = password_verify($pwd, $row['user_pwd']);
                    if ($hashedPwdCheck == false) {
                        //header("Location: ".HOME_NOT_LOGGEDIN_URL."?". LOGIN_STATUS_INURL."=".ERROR_INURL);
                        header("Location: ".HOME_NOT_LOGGEDIN_URL);
                        exit();
                    } elseif ($hashedPwdCheck == true) {
                        // Log in the user
                        $_SESSION['user_id'] = $row['user_id'];
                        $_SESSION['user_society'] = $row['user_society'];
                        $_SESSION['user_email'] = $row['user_email'];

                        /*
                        This next shunk of code make it so that we scan the output from the file
                        grizzly.txt every 5 seconds and when we see "Grizzly server running", we
                        know that OTP is running so we hop out of the loop

                        TODO : Make this run in parallel with the rest of the script so
                        the user can do other stuff while OTP is loading
                        IMPORTANT : THIS HAS BEEN DONE (with AJAX) BUT IS NOT FULLY FUNCTIONNAL

                        NOTE : As far as I know, this doesn't work on Windows because we can't
                        redirect command line output to a file
                        */
                        /*
                        $ready = false;
                        while(!$ready){
                            if(strpos(file_get_contents('grizzly.txt'), 'Grizzly server running') !== false){
                                $ready = true;
                            } else {
                                sleep(5);
                            }
                        }
                        */

                        header("Location: " . HOME_LOGGEDIN_URL);
                        exit;
                    }
                }
            }
        }
    } else {
        header("Location: ". HOME_NOT_LOGGEDIN_URL);
        exit();
    }
 ?>
