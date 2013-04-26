#!/usr/bin/env python

# This file is part of kopo.
#
#  kopo is free software: you can redistribute it and/or
#  modify it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3 of
#  the License, or (at your option) any later version.
#
#  kopo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public
#  License along with kopo. If not, see
#  <http://www.gnu.org/licenses/>.
#
# (C) 2012- by Stefan Marsiske <s@ctrlc.hu>, Adam Tauber <asciimoo@faszkorbacs.hu>

from flask import Flask, request, render_template, Response
from common import cfg
from whois import whois, save
import json, tempfile, os
import pygeoip

gi = pygeoip.GeoIP('GeoIPCity.dat')

# todo maybe there's a better way to do it
cache_persistence_period=3 # save cache on every 3rd request
cache_persistence_counter=0

torexits=[]
with open('torexits.csv', 'r') as fp:
    torexits=[x.strip() for x in fp]

app = Flask(__name__)
app.secret_key = cfg.get('app', 'secret_key')

vendormap={"windows": "Microsoft",
          "linux": "Linux",}

@app.context_processor
def contex():
    global cfg, query
    return {'cfg'   : cfg
           ,'query' : ''
           ,'path'  : request.path
           }

def getISP(ip):
    tmp=gi.record_by_addr(ip)
    if ip in torexits:
        return tmp['city'], tmp['country_name'], "TOR"
    if tmp:
        return tmp['city'], tmp['country_name'], whois(ip)[-1]
    tmp=whois(ip)
    if tmp:
        return 'unknown', 'unknown', tmp[-1]
    return 'unknown', 'unknown', ip

def colorize(o):
    for k,i in o.iteritems():
        i['color']="#%02x%02x00" % ((100-i['q'])*255//100, i['q']*255//100)
    return o

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/kopo.js', methods=('GET',))
def kopojs():
    global cache_persistence_counter
    #platform=request.args.get('platform',request.user_agent.platform)
    ip=request.args.get('ip',request.headers.get('x-forwarded-for', request.remote_addr))

    city, country, isp = getISP(ip)
    cache_persistence_counter+=1
    if cache_persistence_counter % cache_persistence_period == 0:
        save()

    # etag tracking, saves in /tmp/kopo-etag-XXX..
    tmpf=None
    evisits=[]
    if request.if_none_match:
        etag=request.if_none_match.to_header()[1:-1]
        if len(etag)==len(''.join([x for x
                                   in etag
                                   if x.isalnum() or x in ['_']])):
            tmpf='/tmp/kopo-etag-'+etag
            try:
                with open(tmpf,'r') as fd:
                    evisits=[x.strip() for x in fd.readlines()]
            except:
                tmpf=None
            else:
                evisits.append(request.referrer or "unknown")
                with open(tmpf,'w') as fd:
                    fd.write('\n'.join(evisits))
    if not tmpf:
        # initalize etag storage
        evisits=[request.referrer or "unknown"]
        fd, tmpf = tempfile.mkstemp(prefix="kopo-etag-")
        with os.fdopen(fd,'w') as f:
            f.write('\n'.join(evisits))
        etag=tmpf[len("/tmp/kopo-etag-"):]
    resp = Response(render_template('kopo.js'
                                   ,vendor=vendormap.get(request.user_agent.platform,request.user_agent.platform)
                                   ,isp=isp
                                   ,city=city
                                   ,evisits=json.dumps(evisits or [])
                                   ,country=country
                                   )
                   ,mimetype='text/javascript'
                   )
    # set a cookie
    resp.set_cookie('visits',int(request.cookies.get('visits',0))+1)
    # set etag id
    resp.headers['ETag']=etag
    return resp

if __name__ == "__main__":
    app.run(debug        = cfg.get('server', 'debug')
           ,use_debugger = cfg.get('server', 'debug')
           ,port         = int(cfg.get('server', 'port'))
           )
