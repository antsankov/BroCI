#!/usr/bin/python

import subprocess,time

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
	
	def print_all(self):
		print('NETSTAT')
                print("Device: {}".format(self.device))
                print("Time: {}".format(self.time))
                print("Recvd: {}".format(self.recvd))
                print("Dropped: {}".format(self.dropped)) 
                print("Link: {}".format(self.link))
		print('======')

class capstat: 

	def __init__(self,interface,kbps,mbps,avg):
		self.interface = interface
		self.kbps = kbps
		self.mbps = mbps
		self.avg = avg

	def print_all(self):
		print('CAPSTAT')
		print("Interface: {}".format(self.interface))
		print("kbps: {}".format(self.kbps))
		print("mbps: {}".format(self.mbps))
		print("avg: {}".format(self.avg))
		print('------')

def collect_netstats():

	#Output comes out like: 'bro: 1423522199.184053 recvd=22756 dropped=4071 link=26827'
	netstats_string = subprocess.check_output('sudo /usr/local/bro/bin/broctl netstats', shell=True)
	netstats_split = netstats_string.strip().replace(':','').replace('recvd=','').replace('dropped=','').replace('link=','').split()
	netstat_snapshot = netstat(netstats_split[0],netstats_split[1],netstats_split[2],netstats_split[3],netstats_split[4])
	
	return netstat_snapshot

def collect_capstats():
	capstats_snapshot = []
	#capstats seems to output on the stderror FD 
	capstats_string = subprocess.check_output('sudo /usr/local/bro/bin/broctl capstats',stderr=subprocess.STDOUT, shell=True)
	#split capstats into multiple lines
	capstats_split_line = capstats_string.splitlines()
	
	#go through the lines for the different interfaces, starting on the third
	for i in range (3, len(capstats_split_line)):
		#split on the words
		capstats_split_word = capstats_split_line[i].split()
		#instatiate a capstats_snapshot for each of the interfaces and add it to our capstats_snapshot list 
		try: 
			capstats_snapshot.append(capstat(capstats_split_word[0],capstats_split_word[1],capstats_split_word[2],capstats_split_word[3]))
		#if there is no traffic, the avg is simply null
		except: 
			capstats_snapshot.append(capstat(capstats_split_word[0],capstats_split_word[1],capstats_split_word[2],0))
	
	return capstats_snapshot

def main():	
	starttime=time.time()
	
	netstat_snapshots = []
	capstat_snapshots = []
	collect_capstats()
	#this collects a snapshot every ten seconds 
	while True:
		capstat_snapshot = collect_capstats()
		capstat_snapshots.append(capstat_snapshot)
		capstat_snapshot[0].print_all()
		
		netstat_snapshot = collect_netstats()
		netstat_snapshots.append(netstat_snapshot)
		netstat_snapshot.print_all()
	
		time.sleep(10.0 - ((time.time() - starttime) % 10.0))

if __name__ == "__main__": 
	main()
