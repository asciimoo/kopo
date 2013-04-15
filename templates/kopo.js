
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
        var tc = '<thead><tr><td>freedom</td><td>score</td><td>explanation</td></tr></thead><tbody>';
        for(i in scores) {
            tc += '<tr><td>';
            if(scores[i].url) {
                tc += '<a href="'+scores[i].url+'">'+scores[i].title+'</a>';
            } else {
                tc += scores[i].title;
            }
            tc += '</td><td style="background: '+scores[i].color+'" title="'+scores[i].text+'">'+scores[i].q+'</td>';
            tc += '<td>'+scores[i].text+'</td></tr>';
        }
        tc += '</tbody>';
        var table = document.createElement('table');
        table.innerHTML = tc;
        target.appendChild(table);
    }
    if(prev_onload_callback)
        return prev_onload_callback();
}

window.onload = init;
