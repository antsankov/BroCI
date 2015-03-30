# Intro 

This is a collection of BRO scripts and pcap files that I will use to profile bro performance. 
This readme is mainly for my own personal notes where I can log interesting commands and file locations. 

# Notes

* Run ```install``` on broctl after it's been freshly installed. 
* Change loaded scripts in local.bro

## Commands
* Tcpreplay sample command on n0: ```sudo tcpreplay --topspeed --loop=0 --intf1=eth2 c1_final.pcap```
* Convert file to be transmitted fron n0: ```tcprewrite --dstipmap=0.0.0.0/0:10.1.1.3 --enet-dmac=00:04:23:b7:41:f0 --srcipmap=0.0.0.0/0:10.1.1.2 --enet-smac=00:04:23:a8:da:62 --fixcsum --infile=browse.pcap --outfile=temp1.pcap ```

## Locations
* Logs: ```/usr/local/bro/logs```
* Local.bro and other scripts to be used by broctl are stored in: ```/usr/local/bro/share/bro/site```
* Store actual broscript ref'd by local.bro in: ```/usr/local/bro/share/bro/policy/misc```
* Change node config in: ```/usr/local/bro/etc/```

## Profiler
The profiler module (profiler.bro) is stored in ```/usr/local/bro/share/bro/site```. There should be an entry in local.bro for it with the line ```@load profiler.bro```. 

A log file only appears when someone calls it with the ```log_event(name)``` function.
