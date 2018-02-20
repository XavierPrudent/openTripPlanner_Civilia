
function validateGTFSFile(){

    var file_data = $('#gtfs1').prop('files')[0];
    var form_data = new FormData();
    form_data.append('file', file_data);
    $.ajax({
            url: '<?PHP echo VALIDATE_FILE_PHP_FILE?>', // point to server-side PHP script
            dataType: 'text',  // what to expect back from the PHP script, if anything
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,
            type: 'POST',
            success: function(php_script_response){
            alert(php_script_response); // display response from the PHP script, if any
        }
    });

    /*
    if (city = <?php echo SELECT_CITY_DEFAULT?>) {
        // TODO : Error handling
    } else {
        var gtfs = document.getElementById('gtfs1').value;
        if (gtfs == "") {
            // TODO : Error handling
        } else {
            // TODO 1 : make sure that we can pass a file this way
            // TODO 2 : Make this a POST
            // TODO 3 : get the real osm file
            xmlHttp.open("GET", <?php echo LOADOTP_PHP_FILE?> . '?gtfs=' . gtfs . '?osm=' . gtfs, true);
            xmlHttp.onreadystatechange = handleServerResponseOTPload;
            xmlHttp.send(null);
        }
    }
    */
}

function handleServerResponseOTPload(){
    if (xmlHttp.readyState == 4){
	console.log('State is 4.');
        if (xmlHttp.status == 200){
	    console.log('Status good. Handling server response.');
            xmlResponse = xmlHttp.responseXML;
            xmlDocumentElement = xmlResponse.documentElement;
            response = xmlDocumentElement.firstChild.data;
	    if (response == 'true'){
            document.getElementById('<?php OTP_BUTTON_TEXT ?>').classList.remove('disabled');
	    	console.log('All done. OTP button class has been changed');
	    }
        } else {
	    console.log('Status is ' + xmlHttp.status);
	    alert(xmlHttp.responseText);
	}
    } else {
	console.log(xmlHttp.readyState);
        console.log('OpenTripPlanner is not done loading.');
	    setTimeout('waitOTPload()', 2000);
    }
}
