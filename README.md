# Intro 

This is a collection of BRO scripts and pcap files that I will use to profile bro performance. 
This readme is mainly for my own personal notes where I can log interesting commands and file locations. 

# Notes

* Run ```install``` on broctl after it's been freshly installed. 
* Change loaded scripts in local.bro

## Commands
Tcpreplay sample command: ```sudo tcpreplay -i eth0 -tK --loop 100000 browse.pcap```

## Locations
* Logs: ```/usr/local/bro/logs```
* Local.bro and other scripts to be used by broctl are stored in: ```/usr/local/bro/share/bro/site```
* Store actual broscript ref'd by local.bro in: ```/usr/local/bro/share/bro/policy/misc```
* Change node config in: ```/usr/local/bro/etc/```
