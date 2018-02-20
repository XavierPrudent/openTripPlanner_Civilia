<?php

header('Content-Type: text/xml');
echo '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>';

/*
if (filesize('grizzly.txt') == 0){
    //Use this next line on Unix server
    // exec(OTP_CMD_LINE . " > grizzly.txt &");

    // Use these next 2 lines on a Windows server
    // $shell = new COM("WScript.Shell");
    // $shell->Exec(OTP_CMD_LINE);
}
*/

echo '<response>';
    if (strpos(file_get_contents('grizzly.txt'), 'Grizzly server running.') === false) {
	       echo 'false';
    } else {
	       echo 'true';
    }
echo '</response>';

 ?>
