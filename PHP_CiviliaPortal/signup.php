<?php
    require('config/config.php');
    require('config/db.php');

    // Check For Submit
    if(isset($_POST['submit'])){
        // Get from data
        $society = mysqli_real_escape_string($conn, $_POST['society']);
        $email = mysqli_real_escape_string($conn, $_POST['email']);
        $pwd = mysqli_real_escape_string($conn, $_POST['password']);
        $confirm_pwd = mysqli_real_escape_string($conn, $_POST['passwordconfirm']);

        if (empty($society) || empty($email) || empty($pwd)  || empty($confirm_pwd)){
            header('Location: ' . SIGNUP_PAGE_URL . '?'. SIGNUP_STATUS_INURL.'='.SIGNUP_EMPTY_INURL);
            exit();
        } else {
            if (!filter_var($email, FILTER_VALIDATE_EMAIL)){
                // validate email format

                // TODO : verify email address by sending email

                header('Location: ' . SIGNUP_PAGE_URL . '?'.SIGNUP_STATUS_INURL.'='.SIGNUP_INVALID_EMAIL_INURL);
                exit();
            } else {
                $query = "SELECT * FROM users WHERE " . TABLE_USERS_EMAIL_COL_NAME . "='$email'";
                $result = mysqli_query($conn, $query);
                $resultCheck = mysqli_num_rows($result);

                if($resultCheck > 0) {
                    // Only 1 user per email
                    header('Location: ' . SIGNUP_PAGE_URL . '?'. SIGNUP_STATUS_INURL.'='. SIGNUP_EMAIL_USED_INURL);
                    exit();
                } else {
                    if ($pwd !== $confirm_pwd) {
                        // Password and confirmation password need to be identical
                        header('Location: ' . SIGNUP_PAGE_URL . '?' . SIGNUP_STATUS_INURL . '=' . SIGNUP_NONIDENTIC_PWD_INURL);
                        exit();
                    } else {
                        $hashedPwd = password_hash($pwd, PASSWORD_DEFAULT);
                        $query = "INSERT INTO " . TABLE_USERS_ALL_BUT_ID . " VALUES('$society', '$email', '$hashedPwd')";

                        if(mysqli_query($conn, $query)){
                            header('Location: ' . SIGNUP_PAGE_URL . '?'.SIGNUP_STATUS_INURL.'='.SUCCESS_INURL);
                        } else {
                            echo 'ERROR: ' . mysqli_error($conn);
                        }
                    }
                }
            }
        }
    }

?>

<?php include('inc/header.php'); ?>
    <div class="jumbotron text-center">
        <h1 class="display-3"><?php echo SIGNUP_PAGE_NAME?></h1>
        <hr class="my-4">
        <form action="<?php $_SERVER['PHP_SELF'];?>" method="POST">
            <input class="form-group form-control" type="text" name="society"
                placeholder="<?php echo SOCIETY_PLACEHOLDER;?>" value='<?php echo isset($_POST['SIGNUP_POST_EMAIL']) ? $_POST['SIGNUP_POST_EMAIL'] : "";?>'>
            <?php if ( isset($_GET[SIGNUP_STATUS_INURL]) && $_GET[SIGNUP_STATUS_INURL] == SIGNUP_EMAIL_USED_INURL):?>
                <div class="alert alert-dismissible alert-danger">
                    <?php echo SIGNUP_EMAIL_USED_MESSAGE; ?>
                </div>
            <?php endif; ?>
            <input class="form-group form-control" id="exampleInputEmail1" aria-describedby="emailHelp"
            type="text" name="email" placeholder="<?php echo EMAIL_PLACEHOLDER;?>">
            <?php if ( isset($_GET[SIGNUP_STATUS_INURL]) && $_GET[SIGNUP_STATUS_INURL] == SIGNUP_NONIDENTIC_PWD_INURL):?>
                <div class="alert alert-dismissible alert-danger">
                    <?php echo SIGNUP_NONIDENTIC_PWD_MESSAGE; ?>
                </div>
            <?php endif; ?>
            <input class="form-group form-control" id="exampleInputPassword1"
                type="password" name="password" placeholder="<?php echo PWD_PLACEHOLDER;?>">
            <input class="form-group form-control" id="exampleInputPassword1"
                type="password" name="passwordconfirm" placeholder="<?php echo PWD_CONFIRM_PLACEHOLDER;?>">
            <button class="btn btn-primary" type="submit" name="submit"><?php echo SIGNUP_BUTTON_TEXT;?></button>
        </form>
    </div>

<?php include('inc/footer.php'); ?>
