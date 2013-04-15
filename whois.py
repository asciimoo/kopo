#!/usr/bin/env python

# src http://code.activestate.com/recipes/576635-whois/

import sys
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

load()
#print whois("80.99.33.212")
#print whois("80.99.239.111")
#print whois("80.99.32.211")
#print whois("70.99.32.211")
#print whois("170.99.32.211")
#save()
