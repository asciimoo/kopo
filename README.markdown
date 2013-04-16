KOPO
====


### Dependencies

 * python2.7
 * [Flask](flask.pocoo.org)
 * msgpack-python
 * pygeoip

### acquire data files

    curl 'http://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv' -o data/torexits.csv
    curl 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity-latest.tar.xz' | xz -dc >GeoIPCity.dat
