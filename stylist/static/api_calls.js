/* 
 * API call wrapper.
 * Retry API calls up to 10 times using ScriptCaller.
 * Call callback function if success.
 * Callback function gets data and retry function parameters.
 */
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
