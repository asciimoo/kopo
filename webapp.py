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
import json
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

@app.route('/', methods=['GET'])
def index():
    print request.user_agent
    return render_template('index.html')

@app.route('/kopo.js', methods=('GET',))
def kopojs():
    global cache_persistence_counter
    platform=request.args.get('platform',request.user_agent.platform)
    ip=request.args.get('ip',request.headers.get('x-forwarded-for', request.remote_addr))
    city, country, isp = getISP(ip)
    cache_persistence_counter+=1
    if cache_persistence_counter % cache_persistence_period == 0:
        save()
    return Response(render_template('kopo.js'
                                   ,vendor=request.user_agent.platform
                                   ,isp=isp
                                   ,city=city
                                   ,country=country
                                   )
                   ,mimetype='text/javascript'
                   )


@app.route('/crypto.html', methods=['GET'])
def crypto():
    return render_template('crypto.html')

if __name__ == "__main__":
    app.run(debug        = cfg.get('server', 'debug')
           ,use_debugger = cfg.get('server', 'debug')
           ,port         = int(cfg.get('server', 'port'))
           )
