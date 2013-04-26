
var vendor = '{{vendor}}';
var isp = '{{isp}}';
var city = '{{city}}';
var country = '{{country}}';
var evisits = {{evisits}};
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

function createElement(type, text, style) {
    var element = document.createElement(type);
    if(text)
        element.innerHTML = text;
    if(style)
        element.style.cssText = style;
    return element;
}

function init() {
    var target = document.getElementById('kopo');
    if(target) {
        target.style.cssText = 'width: 250px; border: 4px solid #000000; text-align: center; padding: 0; margin: 0; background: #FFFFFF; color: #000000; clear: both; font-size: 16px; ';

        target.appendChild(createElement('div', 'You seem to be located in', 'padding: 4px'));
        target.appendChild(createElement('div', city+', '+country, 'font-size: 20px;'));

        target.appendChild(createElement('div', 'You seem to be using a system from', 'padding: 4px;'));
        target.appendChild(createElement('div', vendor, 'font-size: 30px;'));

        target.appendChild(createElement('div', 'and use a network provider', 'padding: 4px;'));
        target.appendChild(createElement('div', isp, 'font-size: 30px;'));

        var cvisits = getCookie('visits');
        if(!cvisits) cvisits = 0;
        target.appendChild(createElement('div', " We also routinely record your IP address and your surfing habits. And there's a few more ways to track you, which we haven't implemented.", 'padding: 4px;'));

        target.appendChild(createElement('div', 'You have been seen by this widget', 'background: #000000; color: #FFFFFF; padding-top: 4px;'));
        target.appendChild(createElement('div', ""+Math.max(evisits.length, cvisits), 'background: #000000; color: #FFFFFF; font-size: 44px;'));
        target.appendChild(createElement('div', 'time(s)', 'background: #000000; color: #FFFFFF; text-align: center; padding-bottom: 4px;'));
    }
    if(prev_onload_callback)
        return prev_onload_callback();
}

window.onload = init;
