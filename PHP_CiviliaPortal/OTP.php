<meta charset="UTF-8">

<?php
    require_once('config/config.php');
    require_once('config/db.php');
?>

<!-- This is exactly what is in header.php except for onload="process()", can we make this better? !-->
<!DOCTYPE html>
<html>
<head>
    <title><?php echo PORTAL_NAME?></title>
    <link rel="stylesheet" type="text/css" href="https://bootswatch.com/4/superhero/bootstrap.min.css">
    <script type="text/javascript" src="res/js/jquery-3.1.1.min.js"></script>
    <script type="text/javascript" src="res/js/res_javascript.js"></script>
    <script type="text/javascript" src="res/js/loadOTP.js"></script>
</head>
<body  onload="waitOTPload()">
 <?php include('inc/navbar.php'); ?>
 <!-- end of what is in header.php !-->
    <div class="jumbotron text-center">
        <h1 class="display-3"><?php echo PORTAL_NAME?></h1>
        <p class="lead"><?php echo LONG_EXPL?></p>
        <hr class="my-4">
        <p class="lead">
            <a id="<?php echo OTP_BUTTON_TEXT?>" class="btn btn-success btn-lg disabled" name="otp"
            role="button" href=<?php echo OTP_PAGE_URL ?>><?php echo OTP_BUTTON_TEXT?></a>
        </p>
    </div>

<?php include('inc/footer.php'); ?>
