var xmlHttp = createXmlHttpRequestObject();

function createXmlHttpRequestObject() {
    var xmlHttp;

    if(window.ActiveXObject){
        // if the user uses Internet Explorer
        try {
            xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
        } catch(e) {
            smlHttp = false;
        }
    } else {
        // if the user uses a real browser
        try {
            xmlHttp = new XMLHttpRequest();
	    console.log('User uses real browser');
        } catch (e) {
            xmlHttp = false;
        }
    }
    return xmlHttp;
}
