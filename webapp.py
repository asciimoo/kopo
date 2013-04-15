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
from urlparse import urlparse
import json

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
    return ip

vendors={
    'linux': {
        'Free software': {
          'url': 'https://www.gnu.org/gnu/manifesto.html',
          'q': 100,
          'text': 'your vendor respects you and allows you to access and share your system freely'},
         'Hardware': {
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 90,
           'text': 'your vendor suggests you run on mostly freely hackable hardware'},
         'Cryptography': {
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 90,
           'text': 'your vendor suggests you have many options available encrypting your communications'},
         'Anonymity': {
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 90,
           'text': 'your vendor suggests you have many options to protect your identity online'},
         'Security': {
          'q': 70,
          'text': 'your vendor allows for many various security defences'},
         },
    'windows': {
         'Free Software': {
           'url': 'https://www.gnu.org/gnu/manifesto.html',
           'q': 0,
           'text': 'your vendor disrespects you and mostly prohibits access to the source of the system'},
         'Hardware': {
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 90,
           'text': 'your vendor suggests you run on mostly freely hackable hardware'},
         'Cryptography': {
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 10,
           'text': 'your vendor provides barely any encryption tools'},
         'Anonymity': {
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 0,
           'text': 'your vendor provides no tools protect your identity online'},
         'Security': {
          'q': 70,
          'text': 'your vendor provides many disabled-by-default defences'},
        },
    'macos': {
         'Free Software': {
           'url': 'https://www.gnu.org/gnu/manifesto.html',
           'q': 5,
           'text': 'your vendor disrespects you while it allows access to the kernel, but not the rest of the system.'},
         'Hardware': {
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 5,
           'text': 'your vendor nowadays shows total contempt for it\'s users, it does not even allow you to unscrew the case of your device'},
         'Cryptography': {
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 10,
           'text': 'your vendor provides barely any encryption tools'},
         'Anonymity': {
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 0,
           'text': 'your vendor provides no tools protect your identity online'},
         'Security': {
          'q': 20,
          'text': 'your vendor neglects security in favor of shiny pebbles'},
        },
    'iphone': {
         'Free Software': {
           'url': 'https://www.gnu.org/gnu/manifesto.html',
           'q': 0,
           'text': 'your vendor disrespects you barring access to the source our your system.'},
         'Hardware': {
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 0,
           'text': 'your vendor nowadays shows total contempt for it\'s users right to access the hardware.'},
         'Cryptography': {
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 10,
           'text': 'your vendor provides barely any encryption tools'},
         'Anonymity': {
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 0,
           'text': 'your vendor provides no tools protect your identity online'},
         'Security': {
          'q': 20,
          'text': 'your vendor neglects security in favor of shiny pebbles'},
        },
    'android': {
         'Free Software': {
           'url': 'https://www.gnu.org/gnu/manifesto.html',
           'q': 40,
           'text': 'your vendor uses free software, but provides proprietary features.'},
         'Hardware': {
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 90,
           'text': 'your hardware is not really hackable'},
         'Cryptography': {
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 10,
           'text': 'your vendor provides barely any encryption tools'},
         'Anonymity': {
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 0,
           'text': 'your vendor provides no tools protect your identity online'},
         'Security': {
          'q': 40,
          'text': 'your vendor neglects security'},
        },
    'solaris': {
         'Free Software': {
           'url': 'https://www.gnu.org/gnu/manifesto.html',
           'q': 80,
           'text': 'your vendor started respecting you in it\'s late days, but does not exist anymore :('},
         'Hardware': {
           'url': 'http://makezine.com/04/ownyourown/',
           'q': 90,
           'text': 'your vendor suggests you run on mostly freely hackable hardware'},
         'Cryptography': {
           'url': 'http://activism.net/cypherpunk/crypto-anarchy.html',
           'q': 10,
           'text': 'your vendor provides barely any encryption tools'},
         'Anonymity': {
           'url': 'https://www.un.org/en/documents/udhr/index.shtml#a12',
           'q': 0,
           'text': 'your vendor provides no tools protect your identity online'},
         'Security': {
          'q': 20,
          'text': 'your vendor once provided proprietary defences'},
         },
    'unknown': {
        'Free Software': {
           'q': 50,
           'text': 'unknown'},
        'Hardware' : {
           'q': 50,
           'text': 'unknown'},
        'Cryptography' : {
           'q': 50,
           'text': 'unknown'},
        'Anonymity': {
           'q': 50,
           'text': 'unknown'},
        'Security': {
          'q': 50,
          'text': 'unknown'},
        },
    }

def getFreedoms(vendor):
    global vendors
    freedom = dict(vendors.get(vendor, vendors['unknown']))
    return freedom

def colorize(o):
    for k,i in o.iteritems():
        i['color']="#%02x%02x00" % ((100-i['q'])*255//100, i['q']*255//100)
    return o

@app.route('/', methods=['GET'])
def index():
    print request.user_agent
    return render_template('index.html')

@app.route('/kopo.js', methods=('GET',))
def kopojs():
    platform=request.args.get('platform',request.user_agent.platform)
    ip=request.args.get('ip',request.headers.get('x-forwarded-for', request.remote_addr))
    referrer = urlparse(request.referrer or '')
    url      = urlparse(request.url)
    scores   = getFreedoms(platform)
    if referrer.netloc and url.netloc != referrer.netloc:
        scores['Security']['q'] *= 0.8

    return Response(render_template('kopo.js'
                                   ,vendor=request.user_agent.platform
                                   ,freedoms=json.dumps(colorize(scores))
                                   ,isp=getISP(ip)
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
