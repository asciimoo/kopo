
var vendor = '{{vendor}}';
var isp = '{{isp}}';
var city = '{{city}}';
var country = '{{country}}';
var evisits = '{{evisits}}';
var prev_onload_callback = window.onload;

function getCookie(c_name) {
   var i,x,y,ARRcookies=document.cookie.split(";");
   for (i=0;i<ARRcookies.length;i++) {
      x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
      y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
      x=x.replace(/^\s+|\s+$/g,"");
      if (x==c_name) {
         return unescape(y);
      }
   }
}

function init() {
    var target = document.getElementById('kopo');
    if(target) {
        target.appendChild(document.createTextNode('You have been seen by this widget '+evisits+' times (without cookies!) and seem to be located in '+city+', '+country+'. You seem to be using a system from '+vendor+', and use a network provider '+isp+". "));
    }
    var visits = getCookie('visits');
    if(visits) {
        target.appendChild(document.createTextNode('You also seem to allow cookies and have been seen by this widget '+visits+' time(s).'));
    }
    if(prev_onload_callback)
        return prev_onload_callback();
}

window.onload = init;
