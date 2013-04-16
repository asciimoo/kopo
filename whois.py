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
# (C) 2013- by Stefan Marsiske <s@ctrlc.hu>

import socket
import msgpack
import shutil

cache={}

def ip2int(ip):
    return int(''.join(["%02x" % int(x) for x in ip.split('.')]),16)

def cidrmask(txt):
    block, size=txt.split('/')
    size=int(size)
    mask=ip2int(block)
    return mask, size

def inblock(ip, mask, size):
    if mask == ( ip & ( ((2**32)-1) << (32-size) ) ):
        return True
    return False

def whois(ip):
    ipl=ip2int(ip)
    for mask, size in cache.keys():
        #print "ipl %x, %x, %d" % (ipl, mask, size)
        if inblock(ipl, mask, size):
            return cache[(mask, size)]
    fields=_whois(ip)
    #print 'fields', fields
    if fields[1]:
        mask, size = cidrmask(fields[1])
        cache[(mask,size)]=fields
        #print "mask,s %x, %d " % (mask, size)
        return fields

# src http://code.activestate.com/recipes/576635-whois/
def _whois(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("asn.shadowserver.org", 43))
    s.send("origin %s\r\n" % ip)
    response = ''
    while True:
        d = s.recv(4096)
        response += d
        if d == '':
            break
    s.close()
    #print
    #print response.strip()
    return tuple([x.strip() for x in response.strip().split('|')])

def save(path="whois.cache"):
    global cache
    with open(path+'-new','w') as fd:
        fd.write(msgpack.packb(cache))
    shutil.move(path+'-new',path)

def load(path="whois.cache"):
    global cache
    with open(path,'r') as fd:
        cache=msgpack.unpackb(fd.read(),use_list=False)

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2 and argv[1] == 'init':
        save()
load()
