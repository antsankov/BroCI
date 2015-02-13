#!/usr/bin/python

import subprocess,time


class netstat:

	'''Output of each device reutrned by 'broctl netstats': 

	bro: 1423861198.685558 recvd=25118568 dropped=69563523 link=94682096

	Contains information about the following- 
		
		device : what is the name of the device, defined in node.cfg 
		time: the time that the measurment was taken, in Unix epoc time
		recvd: this is the number of packets that have been successfully analyzed 
		dropped: these are packets that are dropped due to lack of resources 
		link: these are the total number of packets that have been recieved, regardless of whether they have been analyzed
	'''		
			
	def __init__(self, device, time, recvd, dropped,link):
		self.device = device
		self.time = time
		self.recvd = float(recvd)
		self.dropped = float(dropped) 
		self.link = float(link)
	
	''' Sanity check if the number of dropped and recvd matches number of packets on the link '''
	def confirm(self):
		if (self.recvd + self.dropped != self.link):
			return False
		else:
			return True 

	''' Loss rate percentage is determiend by dropped divided by total on link'''  
	def loss_rate(self):
		return (self.dropped / self.link)

	''' Success rate percentage is determiend by success divided by total on link'''  
	def success_rate(self):
		return (self.recvd / self.link)
	
	''' Prints all of the useful information conatined in this object, useful for debugging purposes'''
	def print_all(self):
		print('NETSTAT')
                print("Device: {}".format(self.device))
                print("Time: {}".format(self.time))
                print("Recvd: {}".format(self.recvd))
                print("Dropped: {}".format(self.dropped)) 
                print("Link: {}".format(self.link))
		print('======')

class capstat: 
	'''Output of link information returned by 'broctl snapshots', based on a 10s average: 

	localhost/eth2        36.3       25.6
	
	Contains information about the following- 
	
		host/inteface : the inteface of the device being meauserd (TODO - possibly split these into two other object variables)
		kpps : 10s avg of number of kpps on the link
		mbps : 10s avg of speed rate on the link
		
	'''

	def __init__(self,interface,kpps,mbps):
		self.interface = interface
		self.kpps = kpps
		self.mbps = mbps
		
	''' Prints all of the useful information conatined in this object, useful for debugging purposes'''
	def print_all(self):
		print('CAPSTAT')
		print("Interface: {}".format(self.interface))
		print("kpps: {}".format(self.kpps))
		print("mbps: {}".format(self.mbps))	
		print('------')

def collect_netstats():
	''' This function reutrns an array of netstat objects for each bro device returned by 'broctl netstats'.
	
	[BroControl] > netstats
        	bro: 1423861198.685558 recvd=25118568 dropped=69563523 link=94682096 
        	shmo: 1423861198.685558 recvd=500 dropped=1337 link=1837
	
	This would create two netstat objects, bro and shmo, put them into an array, the netstats_snapshot, and return the array
	'''
	netstats_snapshot = []
	
	netstats_string = subprocess.check_output('sudo /usr/local/bro/bin/broctl netstats', shell=True)
	
	#split on the new lines for each of the devices 
	netstats_split_line = netstats_string.splitlines()
	
	for i in range (0,len(netstats_split_line)):
		#remove the unwanted characters 
		netstats_split = netstats_string.strip().replace(':','').replace('recvd=','').replace('dropped=','').replace('link=','').split()
		#instantiate the object and add it to the array to be returned 
		netstats_snapshot.append(netstat(netstats_split[0],netstats_split[1],netstats_split[2],netstats_split[3],netstats_split[4]))
	
	return netstats_snapshot

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
		
		if (len(capstats_split_word) is 0):
			print('0 length capstats!')
			return 
		#instatiate a capstats_snapshot for each of the interfaces and add it to our capstats_snapshot list 
		capstats_snapshot.append(capstat(capstats_split_word[0],capstats_split_word[1],capstats_split_word[2]))
	
	return capstats_snapshot


def analyze_netstats(netstat_snapshots):
	
	total_success = 0

	for netstat_snapshot in netstat_snapshots:
		total_success += netstat_snapshot[0].success_rate()  	

	avg_success = (total_success/len(netstat_snapshots))

	print("Avg success: {}".format(avg_success))	
	print("Avg failure: {}".format(1 - avg_success))
	
	return True

def main():	
	starttime=time.time()

	#this is a collection of snapshots collected every  	
	netstat_snapshots = []
	capstat_snapshots = []
		
	#this collects a snapshot every ten seconds 
	while True:
		
		netstat_snapshot = collect_netstats()
		netstat_snapshots.append(netstat_snapshot)
		netstat_snapshot[0].print_all()
	

#		capstat_snapshot = collect_capstats()
#		capstat_snapshots.append(capstat_snapshot)
#		capstat_snapshot[0].print_all()
	
		analyze_netstats(netstat_snapshots)
		time.sleep(5.0 - ((time.time() - starttime) % 5.0))

if __name__ == "__main__": 
	main()
