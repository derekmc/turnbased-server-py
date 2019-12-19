
var REFRESH_TIME = 15*1000;
// idle after 2.5 minutes.
var IDLE_TIMEOUT = 2.5 * 60 * 1000;
//var IDLE_TIMEOUT = 0.2 * 60 * 1000;
var MAXIMUM_AUTO_REFRESH = IDLE_TIMEOUT/REFRESH_TIME;
var REFRESH_PARAM = "r";


window.addEventListener("load", refresh_init);

function refresh_init(){
	MAXIMUM_AUTO_REFRESH = Math.floor(IDLE_TIMEOUT / REFRESH_TIME);
    setTimeout(refresh_timeout, REFRESH_TIME);
}

function getQueryVariable(variable) { // stackoverflow.com/questions/2090551/
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
	return null;
    console.log('Query variable %s not found', variable);
}

function refresh_timeout(){
	var refresh_count = getQueryVariable(REFRESH_PARAM);
	refresh_count = refresh_count? parseInt(refresh_count) : 0;
    if(refresh_count >= MAXIMUM_AUTO_REFRESH){
        refresh_idle_page(); }
    else{
        window.location.replace(window.location.pathname + "?" + REFRESH_PARAM + "=" + (refresh_count + 1)); }
}
function refresh_idle_page(){
    document.body.classList.add("idle");
}

