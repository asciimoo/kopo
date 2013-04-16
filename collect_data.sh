#!/bin/sh

curl 'http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv' -o torexits.csv

curl 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz' | gunzip > GeoIPCity.dat

python whois.py init
