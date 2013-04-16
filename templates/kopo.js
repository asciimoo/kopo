
var vendor = '{{vendor}}';
var isp = '{{isp}}';
var city = '{{city}}';
var country = '{{country}}';
var prev_onload_callback = window.onload;

function init() {
    var target = document.getElementById('kopo');
    if(prev_onload_callback) prev_onload_callback();
    if(!target) return
    target.appendChild(document.createTextNode('You seem to be located in '+city+', '+country+'. You seem to be using a system from '+vendor+', and use a network provider '+isp));
}

window.onload = init;
