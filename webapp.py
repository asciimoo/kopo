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

vendors={
    'linux': [
        { 'title': 'Free software',
          'url': 'https://www.gnu.org/gnu/manifesto.html',
          'q': 100,
          'text': 'your vendor respects you and allows you to access and share your system freely'},
         { 'title': 'Hardware',
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 90,
           'text': 'your vendor suggests you run on mostly freely hackable hardware'},
         { 'title': 'Cryptography',
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 90,
           'text': 'your vendor suggests you have many options available encrypting your communications'},
         { 'title': 'Anonymity',
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 90,
           'text': 'your vendor suggests you have many options to protect your identity online'},
        { 'title': 'Security',
          'q': 70,
          'text': 'your vendor allows for many various security defences'},
         ],
    'windows': [
         { 'title': 'Free Software',
           'url': 'https://www.gnu.org/gnu/manifesto.html',
           'q': 0,
           'text': 'your vendor disrespects you and mostly prohibits access to the source of the system'},
         { 'title': 'Hardware',
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 90,
           'text': 'your vendor suggests you run on mostly freely hackable hardware'},
         { 'title': 'Cryptography',
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 10,
           'text': 'your vendor provides barely any encryption tools'},
         { 'title': 'Anonymity',
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 0,
           'text': 'your vendor provides no tools protect your identity online'},
        { 'title': 'Security',
          'q': 70,
          'text': 'your vendor provides many disabled-by-default defences'},
         ],
    'macos': [
         { 'title': 'Free Software',
           'url': 'https://www.gnu.org/gnu/manifesto.html',
           'q': 5,
           'text': 'your vendor disrespects you while it allows access to the kernel, but not the rest of the system.'},
         { 'title': 'Hardware',
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 5,
           'text': 'your vendor nowadays shows total contempt for it\'s users, it does not even allow you to unscrew the case of your device'},
         { 'title': 'Cryptography',
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 10,
           'text': 'your vendor provides barely any encryption tools'},
         { 'title': 'Anonymity',
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 0,
           'text': 'your vendor provides no tools protect your identity online'},
        { 'title': 'Security',
          'q': 20,
          'text': 'your vendor neglects security in favor of shiny pebbles'},
         ],
    'iphone': [
         { 'title': 'Free Software',
           'url': 'https://www.gnu.org/gnu/manifesto.html',
           'q': 0,
           'text': 'your vendor disrespects you barring access to the source our your system.'},
         { 'title': 'Hardware',
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 0,
           'text': 'your vendor nowadays shows total contempt for it\'s users right to access the hardware.'},
         { 'title': 'Cryptography',
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 10,
           'text': 'your vendor provides barely any encryption tools'},
         { 'title': 'Anonymity',
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 0,
           'text': 'your vendor provides no tools protect your identity online'},
        { 'title': 'Security',
          'q': 20,
          'text': 'your vendor neglects security in favor of shiny pebbles'},
         ],
    'android': [
         { 'title': 'Free Software',
           'url': 'https://www.gnu.org/gnu/manifesto.html',
           'q': 40,
           'text': 'your vendor uses free software, but provides proprietary features.'},
         { 'title': 'Hardware',
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 90,
           'text': 'your hardware is not really hackable'},
         { 'title': 'Cryptography',
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 10,
           'text': 'your vendor provides barely any encryption tools'},
         { 'title': 'Anonymity',
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 0,
           'text': 'your vendor provides no tools protect your identity online'},
        { 'title': 'Security',
          'q': 40,
          'text': 'your vendor neglects security'},
         ],
    'solaris': [
         { 'title': 'Free Software',
           'url': 'https://www.gnu.org/gnu/manifesto.html',
           'q': 80,
           'text': 'your vendor started respecting you in it\'s late days, but does not exist anymore :('},
         { 'title': 'Hardware',
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 90,
           'text': 'your vendor suggests you run on mostly freely hackable hardware'},
         { 'title': 'Cryptography',
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 10,
           'text': 'your vendor provides barely any encryption tools'},
         { 'title': 'Anonymity',
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 0,
           'text': 'your vendor provides no tools protect your identity online'},
        { 'title': 'Security',
          'q': 20,
          'text': 'your vendor once provided proprietary defences'},
         ],
    'unknown': [
         { 'title': 'Free Software',
           'q': 50,
           'text': 'unknown'},
         { 'title': 'Hardware',
           'q': 50,
           'text': 'unknown'},
         { 'title': 'Cryptography',
           'q': 50,
           'text': 'unknown'},
         { 'title': 'Anonymity',
           'q': 50,
           'text': 'unknown'},
        { 'title': 'Security',
          'q': 50,
          'text': 'unknown'},
         ],
    }

def getFreedoms(vendor):
    global vendors
    freedom=vendors.get(vendor, vendors['unknown'])
    for f in freedom:
        f['color']="#%02x%02x00" % ((100-f['q'])*255//100, f['q']*255//100)
    return freedom

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
                                   ,freedoms=json.dumps(getFreedoms(platform))
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
