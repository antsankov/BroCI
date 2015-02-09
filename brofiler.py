#!/usr/bin/python

import sched, time
import subprocess

class netstat:
	
	def __init__(self, device, time, recvd, dropped,link):
		self.device = device
		self.time = time
		self.recvd = float(recvd)
		self.dropped = float(dropped) 
		self.link = float(link)
	
	def confirm(self):
		if (self.recvd + self.dropped != self.link):
			return False
		else:
			return True 
	
	def loss_rate(self):
		return (self.dropped / self.link)

	def success_rate(self):
		return (self.recvd / self.link)

def collect_netstats():

	#Output comes out like: 'bro: 1423522199.184053 recvd=22756 dropped=4071 link=26827'
	netstats_string = subprocess.check_output('sudo /usr/local/bro/bin/broctl netstats', shell=True)
	netstats_split = netstats_string.strip().replace(':','').replace('recvd=','').replace('dropped=','').replace('link=','').split()
	netstat_snapshot = netstat(netstats_split[0],netstats_split[1],netstats_split[2],netstats_split[3],netstats_split[4])
	
	return netstat_snapshot

def main():	
	starttime=time.time()
	netstat_snapshots = []
	#this collects a snapshot every ten seconds 
	while True:
		netstat_snapshot = collect_netstats()
		netstat_snapshots.append(netstat_snapshot)
		print  netstat_snapshot.recvd
		print  netstat_snapshot.confirm()
		print  netstat_snapshot.loss_rate()
		print  netstat_snapshot.success_rate()
		time.sleep(10.0 - ((time.time() - starttime) % 10.0))

if __name__ == "__main__": 
	main()
