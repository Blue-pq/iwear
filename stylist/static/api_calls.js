var retryCounter = 0;

function apiCall(url, callback) {
    function retry(errorMsg) {
        if (retryCounter < 10) {
            setTimeout(() => apiCall(url, callback), 500);
        } else {
            alert(errorMsg);
        }
    }
    retryCounter++;
    OORTLE.ScriptCaller.call(url, function gotit(success, response, id) {
        if (success) {
            callback(response, retry);
        } else {
            retry("Problem reaching the server. Try again later.");
        }
    });
}
