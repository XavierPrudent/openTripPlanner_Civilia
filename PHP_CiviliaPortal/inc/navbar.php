<?php
    session_start();
    require_once('config/config.php');
    require('config/db.php');

?>

<nav class="navbar navbar-expand navbar-dark bg-dark">
      <a class="navbar-brand" href="<?php echo ROOT_URL ?>"><img src="<?php echo CIVILIA_LOGO_PATH;?>" alt="Civilia Logo" width="150"></img></a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExample02" aria-controls="navbarsExample02" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarsExample02">
        <ul class="navbar-nav mr-auto">
            <?php if (isset($_SESSION['user_id'])):?>
                <li class="nav-item active">
                    <a class="nav-link" href="<?php echo HISTORY_PAGE_URL;?>"><?php echo HISTORY_PAGE_NAME;?><span class="sr-only">(current)</span></a>
                </li>
            <?php endif; ?>
        </ul>

        <div class="form-inline my-2 my-md-0">
            <div class="">
                <?php if (isset($_SESSION['user_id'])):?>
                    <form action="<?php echo LOGOUT_PHP_FILE; ?>" method="POST">
                        <button class="btn btn-outline-warning" type="submit" name="submit"><?php echo LOGOUT_BUTTON_TEXT;?></button>
                    </form>
                <?php else: ?>
                <!-- Execute the php file for login when form is submitted !-->
                    <form action="<?php echo LOGIN_PHP_FILE; ?>" method="POST">
                        <input class="form-control" type="text" name="username" placeholder="<?php echo EMAIL_PLACEHOLDER;?>">
                        <input class="form-control" type="password" name="password" placeholder="<?php echo PWD_PLACEHOLDER;?>">
                        <button class="btn btn-outline-success" type="submit" name="submit"><?php echo LOGIN_BUTTON_TEXT;?></button>
                    </form>
            <?php endif;?>
            </div>
      </div>
      </div>
  </nav><br>
