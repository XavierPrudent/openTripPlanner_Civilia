<?php

    // database
    define('ROOT_URL', 'http://localhost/PHP_CiviliaPortal/');
    define('DB_HOST', 'localhost');
    define('DB_USER', 'root');
    define('DB_PASS', 'TwACRYvsXridZZTj');
    define('DB_NAME', 'devtest-civilia');
    define('TABLE_USERS_NAME', 'users');
    define('TABLE_USERS_ID_COL_NAME', 'user_id');
    define('TABLE_USERS_SOCIETY_COL_NAME', 'user_society');
    define('TABLE_USERS_EMAIL_COL_NAME', 'user_email');
    define('TABLE_USERS_PWD_COL_NAME', 'user_pwd');
    define('TABLE_USERS_ALL_BUT_ID', 'users('.TABLE_USERS_SOCIETY_COL_NAME.','.TABLE_USERS_EMAIL_COL_NAME.','.TABLE_USERS_PWD_COL_NAME.')');


    // general
    define('PORTAL_NAME', 'Portail Civilia');
    define('LONG_EXPL', 'Automatiser OTP et faire des analyses statistiques');
    define('CSS_STYLESHEET', ROOT_URL . 'inc/superhero.css');
    define('UPLOAD_TMP_PATH', ROOT_URL . 'tmp/uploads');

        // navbar
    define('CIVILIA_LOGO_PATH', ROOT_URL.'res/img/CIVILIA_logo_blanc.png');
    // 'PWD_INPUT_PLACEHOLDER' is defined in signup page
    define('LOGIN_BUTTON_TEXT', 'Connexion');
    define('LOGOUT_BUTTON_TEXT', 'Déconnexion');

        // not loggedin home page
    define('SIGNUP_BUTTON_TEXT', "Inscription d'un client");

        // signup page
    define('SIGNUP_PAGE_NAME', 'Inscription');
    define('SIGNUP_PAGE_TEXT', 'Entrez les informations demander pour vous inscrire');
    define('SOCIETY_PLACEHOLDER', 'Société');
    define('EMAIL_PLACEHOLDER', 'Adresse Couriel');
    define('PWD_PLACEHOLDER', 'Mot de passe');
    define('PWD_CONFIRM_PLACEHOLDER', 'Confirmer Mot de Passe');
    define('SIGNUP_EMAIL_USED_MESSAGE', "<strong>Adresse déjà enregistrée.</strong> Il semble que l'addresse courriel entrée à déjà été enregistrée, veuillez en utiliser une autre ou connectez-vous");
    define('SIGNUP_NONIDENTIC_PWD_MESSAGE', "<strong>Mots de passe non identiques.</strong> Les deux mots de passe entrées ne sont pas identiques, veuillez réessayer");

        // history pages
    define('HISTORY_PAGE_NAME', 'Historique');

        // Routing form page
    define('OTP_BUTTON_TEXT', 'Lancer OpenTripPlanner');
    define('OTP_CMD_LINE', 'java -Xmx1G -jar /var/www/html/PHP_CiviliaPortal/res/otp/otp-1.3.0-SNAPSHOT-shaded.jar --build /var/www/html/PHP_CiviliaPortal/res/otp/graphs/3r-REF --inMemory --port 22222 --securePort 22223');
    define('STATS_BUTTON_TEXT', 'Analyse statistique');
    define('SELECT_CITY_DEFAULT','-- Choisir une ville --');

        // in url messages
    define('ERROR_INURL', 'error');
    define('SUCCESS_INURL', 'success');
    define('SIGNUP_STATUS_INURL', 'signup');
    define('SIGNUP_EMAIL_USED_INURL', 'emailused');
    define('SIGNUP_EMPTY_INURL', 'empty');
    define('SIGNUP_INVALID_EMAIL_INURL', 'email');
    define('SIGNUP_NONIDENTIC_PWD_INURL', 'password');
    define('LOGIN_STATUS_INURL', 'login');


    // pages link
    define('HOME_NOT_LOGGEDIN_URL', ROOT_URL . 'home.php');
    define('HOME_LOGGEDIN_URL', ROOT_URL . 'OTP.php');
    define('SIGNUP_PAGE_URL', ROOT_URL . 'signup.php');
    define('HISTORY_PAGE_URL', ROOT_URL . 'index.php');
    define('OTP_PAGE_URL', 'http://localhost:22222');

    // php inc files
    define('LOGIN_PHP_FILE', ROOT_URL . 'inc/login.inc.php');
    define('LOGOUT_PHP_FILE', ROOT_URL . 'inc/logout.inc.php');
    define('LOADOTP_PHP_FILE', ROOT_URL . 'inc/loadOTP.inc.php');
    define('VALIDATE_FILE_PHP_FILE', ROOT_URL . 'inc/fileValidation.inc.php');


?>
