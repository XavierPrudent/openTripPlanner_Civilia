<?php
    require_once('config/config.php');
    require_once('config/db.php');
 ?>


<?php include('inc/header.php'); ?>
    <div class="jumbotron text-center">
        <h1 class="display-3"><?php echo PORTAL_NAME?></h1>
        <p class="lead"><?php echo LONG_EXPL?></p>
        <hr class="my-4">
        <p class="lead">
            <a class="btn btn-success btn-lg" name="signup"
            role="button" href=<?php echo SIGNUP_PAGE_URL ?>><?php echo SIGNUP_BUTTON_TEXT?></a>

        </p>
    </div>

<?php include('inc/footer.php'); ?>
