
var vendor = '{{vendor}}';
var isp = '{{isp}}';
var city = '{{city}}';
var country = '{{country}}';
var scores = {{ freedoms }};
var prev_onload_callback = window.onload;

function init() {
    var target = document.getElementById('kopo');
    if(target) {
        target.appendChild(document.createTextNode('You seem to be located in '+city+', '+country+'. You seem to be using a system from '+vendor+', and use a network provider '+isp));
    }
    if(prev_onload_callback)
        return prev_onload_callback();
}

window.onload = init;
