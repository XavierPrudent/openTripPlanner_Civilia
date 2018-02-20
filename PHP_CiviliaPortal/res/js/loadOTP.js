
// TODO : The process needs to stop when OTP is loaded
// TODO 2 : Maybe add 'disabed' class if OTP is NOT load

function waitOTPload(){
    if (xmlHttp.readyState==0 || xmlHttp.readyState == 4){
        xmlHttp.open("GET", 'http://localhost/PHP_CiviliaPortal/inc/loadOTP.inc.php', true);
        xmlHttp.onreadystatechange = handleServerResponseOTPload;
        xmlHttp.send(null);
	console.log('Request sent');
    } else {
        setTimeout('waitOTPload()', 1000);
    }
}

function handleServerResponseOTPload(){
    if (xmlHttp.readyState == 4){
        if (xmlHttp.status == 200){
            xmlResponse = xmlHttp.responseXML;
            xmlDocumentElement = xmlResponse.documentElement;
            response = xmlDocumentElement.firstChild.data;
	    if (response == 'true'){
            document.getElementById('OTP-button').classList.remove('disabled');
	    }
        } else {
	    console.log('Status is ' + xmlHttp.status);
	    alert(xmlHttp.responseText);
	}
    } else {
	console.log(xmlHttp.readyState);
	    setTimeout('waitOTPload()', 2000);
    }
}
