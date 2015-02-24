#!/usr/bin/python
""" Bro profiler controller """

import subprocess
import time
import json
from pymongo import * 

class system_config(object):

    """Boiler plate code for interacting with the system
    Class variables-

        node_cfg: the lcoation of the node.cfg to be modified by bro_device : /usr/local/bro/etc/node.cfg
        load_bro: the location of the load.bro file where we add scripts :  /misc/XXXX
    """

    def __init__(self, node_cfg, load_bro):
        self.node_cfg = node_cfg
        self.load_bro = load_bro

    def modify_node_config(self, bro_device):
        """ Modify the node config with bro_device information """
        with open(self.node_cfg, 'a') as node_cfg_file:
            node_cfg_file.write(bro_device.config_format())

    def modify_local_file(self, bro_script):
        """Modifies the local.bro script with the location of the new script on manager. Use broctl_refresh to get nodes to use it"""
        with open(self.load_bro, 'a') as local_bro_file:
            # store scripts to be loaded in brofiler directory on the manager.
            local_string = "\n###Brofiler###\n@load brofiler/{0}".format(
                bro_script)
            local_bro_file.write(local_string)

def broctl_install():
    subprocess.check_output(
        'sudo /usr/local/bro/bin/broctl install',
        shell=True)

def broctl_restart():
    subprocess.check_output(
        'sudo /usr/local/bro/bin/broctl restart',
        shell=True)

def broctl_refresh():
    broctl_install()
    broctl_restart()

class bro_device(object):

    """ Used to define the type of bro device we are going to be spinning up. We can create either mangers, proxies, or workers. Only workers require interface information
    Class variables-
        
        name: the name of the device
        role: can either be manger, worker, host, standalone (standalone should only be used for local testing purposes)
        host: the host address
        interface: the interface for bro to observe
    """

    def __init__(self, name, role, host, interface='null'):
        self.name = name
        self.role = role
        self.host = host
        self.interface = interface

    def config_format(self):

        if self.role != ('worker' or 'standalone'):
            return "#\n###OTHER###\n[{0}]\ntype={1}\nhost={2}\n".format(
                self.name,
                self.role,
                self.host)

        else:
            return "#\n###WORKER###\n[{0}]\ntype={1}\nhost={2}\ninterface={3}".format(
                self.name,
                self.role,
                self.host,
                self.interface)

class top(object): 
   
    """Output of each device reutrned by 'broctl top':

    bro          standalone localhost     8292    parent  964M    71M  32%  bro 

    Contains information about the following-

        name : the name of the device  
        time: the time that the measurment was taken, in Unix epoc time, THIS IS THE TIME ON THE BROFILER
        role: the type of device (worker, manager, etc.)
        host: the ip of the device in question  
        pid: the pid of the proces
        proc: whether or not if its a parent/child (possibly useless?)
        vsize: virtual memory assigned to the process (possibly useless?)
        rss: physical memory actually being used
        cpu: the amount of cpu being used by the process
    """
    def __init__(self, time, name, role, host, pid, proc, vsize, rss, cpu):
        self.time = time 
        self.name = name
        self.role = role
        self.host = host 
        self.pid = pid 
        self.proc = proc
        self.vsize = vsize
        self.rss = rss 
        self.cpu = cpu 
        
    def print_all(self):
        """ Prints all of the useful information conatined in this object, useful for debugging purposes"""
        print('TOP')
        print("time: {}".format(self.time))
        print("name: {}".format(self.name)) 
        print("role: {}".format(self.role))
        print("host: {}".format(self.host))
        print("pid: {}".format(self.pid))
        print("proc: {}".format(self.proc))
        print("vsize: {}".format(self.vsize))
        print("rss: {}".format(self.rss))
        print("cpu: {}".format(self.cpu)) 
        print('======')

    def csv_format(self):
        return "{},{},{},{},{},{},{},{},{}\n".format(self.time,self.name,self.role,self.host,self.pid,self.proc,self.vsize,self.rss,self.cpu)

def collect_top():
    
    """ This function reutrns an array of top objects for each bro device returned by 'broctl top'.

    [BroControl] > top
                Name         Type       Host          Pid     Proc    VSize  Rss   Cpu  Cmd
                bro          standalone localhost     8292    parent    1G    71M  32%  bro
                bro          standalone localhost     8294    child    90M    47M  26%  bro
    
    This would create two top objects, bro and shmo, put them into an array, the top_snapshot, and return the array
    """
    top_snapshot = []

    try:
        top_string = subprocess.check_output(
            'sudo /usr/local/bro/bin/broctl top',
            stderr = subprocess.STDOUT,
            shell=True)

        # split on the new lines for each of the devices
        top_split_line = top_string.splitlines()

        start_line = 1

        if "warning: removing stale lock" in top_split_line[0]:
            start_line = 2

        for i in range(start_line, len(top_split_line)):
            # remove the unwanted characters
            top_split = top_split_line[i].strip().split()
            # instantiate the object and add it to the array to be returned
            top_snapshot.append(
                top(
                    time.time(),
                    top_split[0], 
                    top_split[1],
                    top_split[2],
                    top_split[3],
                    top_split[4],
                    convert_size(top_split[5]),
                    convert_size(top_split[6]),
                    top_split[7].replace('%','')))

        with open("top.csv","a") as f: 
            for top_device in top_snapshot: 
                f.write(top_device.csv_format())
	
        return top_snapshot

    except subprocess.CalledProcessError:
        print('FAILED top')


def convert_size(size):
    if "M" in size:
        return int(size.replace('M','')) * 1000000

    if "K" in size:
        return int(size.replace('K','')) * 1000

    if "G" in size:
        return int(size.replace('G','')) * 1000000


class netstat(object):

    """Output of each device reutrned by 'broctl netstats':

    bro: 1423861198.685558 recvd=25118568 dropped=69563523 link=94682096

    Contains information about the following-

        device : what is the name of the device, defined in node.cfg
        time: the time that the measurment was taken, in Unix epoc time
        recvd: this is the number of packets that have been successfully analyzed
        dropped: these are packets that are dropped due to lack of resources
        link: these are the total number of packets that have been recieved, regardless of whether they have been analyzed
    """

    def __init__(self, device, time, recvd, dropped, link):
        self.device = device
        self.time = time
        self.recvd = float(recvd)
        self.dropped = float(dropped)
        self.link = float(link)
        self.success = self.success_rate() 
        self.loss = 1 - self.success_rate()

    def success_rate(self):
        if self.link != 0:
            return self.recvd / self.link 
        else:
            return 1 
    def confirm(self):
        """ Sanity check if the number of dropped and recvd matches number of packets on the link """
        if (self.recvd + self.dropped != self.link):
            return False
        else:
            return True

    def print_all(self): 
        print('NETSTAT')
        print("Device: {}".format(self.device))
        print("Time: {}".format(self.time))
        print("Recvd: {}".format(self.recvd))
        print("Dropped: {}".format(self.dropped))
        print("Link: {}".format(self.link))
        print('======')
    
    def csv_format(self):
        return "{},{},{},{},{},{}\n".format(self.time,self.device,self.recvd,self.dropped,self.link,self.success)

def collect_netstats():
    
    """ This function reutrns an array of netstat objects for each bro device returned by 'broctl netstats'.

    [BroControl] > netstats
            bro: 1423861198.685558 recvd=25118568 dropped=69563523 link=94682096
            shmo: 1423861198.685558 recvd=500 dropped=1337 link=1837

    This would create two netstat objects, bro and shmo, put them into an array based on the time, the netstats_snapshot, and return the array
    """
    netstats_snapshot = []

    try:
        netstats_string = subprocess.check_output(
            'sudo /usr/local/bro/bin/broctl netstats',
            shell=True)
        # split on the new lines for each of the devices
        netstats_split_line = netstats_string.splitlines()

        for i in range(0, len(netstats_split_line)):
            # remove the unwanted characters
            netstats_split = netstats_string.strip().replace(
                ':',
                '').replace(
                'recvd=',
                '').replace(
                'dropped=',
                '').replace(
                'link=',
                '').split()
            # instantiate the object and add it to the array to be returned
            netstats_snapshot.append(
                netstat(
                    netstats_split[0],
                    netstats_split[1],
                    netstats_split[2],
                    netstats_split[3],
                    netstats_split[4]))

        with open("netstats.csv","a") as f: 
            for net_device in netstats_snapshot: 
                f.write(net_device.csv_format())
	
        return netstats_snapshot

    except subprocess.CalledProcessError:
        print('FAILED netstats')

class capstat(object):

    """Output of link information returned by 'broctl snapshots', based on a 10s average:

    localhost/eth2        36.3       25.6

    Contains information about the following-

        host/interface : the interface of the device being meauserd (TODO - possibly split these into two other object variables)
        kpps : 10s avg of number of kpps on the link
        mbps : 10s avg of speed rate on the link

    """

    def __init__(self,time, interface, kpps, mbps):
        self.time = time
        self.interface = interface
        self.kpps = kpps
        self.mbps = mbps 

    def print_all(self): 
        print('CAPSTAT')
        print("Interface: {}".format(self.interface))
        print("kpps: {}".format(self.kpps))
        print("mbps: {}".format(self.mbps))
        print('------')

    def csv_format(self):
        return "{},{},{},{}\n".format(self.time,self.interface, self.kpps, self.mbps)

def collect_capstats():
    """This function returns an array of capstat object for each interface returned by 'broctl capstats'

    [BroControl] > capstats

    Interface             kpps       mbps       (10s average)
    ----------------------------------------
    localhost/eth2        36.3       25.6

    This would create a single netstat object, put it into the array capstats_snapshot, and return it.
    """

    capstats_snapshot = []
    # NOTE: capstats seems to output on the stderror FD NOT stdout
   
    
    capstats_string = subprocess.check_output(
        'sudo /usr/local/bro/bin/broctl capstats',
        stderr=subprocess.STDOUT,
        shell=True)
    # split capstats into multiple lines
    capstats_split_line = capstats_string.splitlines()

    # go through the lines for the different interfaces, starting on the third 
    for i in range(3, len(capstats_split_line)):
        # split on the words
        capstats_split_word = capstats_split_line[i].split()

        if (len(capstats_split_word) is 0):
            return

        # instatiate a capstats_snapshot for each of the interfaces and add it
        # to our capstats_snapshot list
        capstats_snapshot.append(
            capstat(
                time.time(),
                capstats_split_word[0],
                capstats_split_word[1],
                capstats_split_word[2]))

    with open("capstats.csv","a") as f: 
        for device_cap in capstats_snapshot:
            f.write(device_cap.csv_format())
    
    return capstats_snapshot
    

def file_init():

    with open('netstats.csv', "wb") as netcsv:
         netcsv.write("Time,Device,Recieved,Dropped,Total,Success\n")

    with open('capstats.csv', "wb") as capcsv: 
        capcsv.write("Time,Interface/Device,kpps,mbps\n")

    with open('top.csv', "wb") as topcsv: 
        topcsv.write("Time,Device,Role,Host,Pid,Proc,VSize,Rss,Cpu\n")

def add_to_db(snapshot,collection):    
    for entry in snapshot:
        json_snapshot = entry.__dict__  
        collection.insert(json_snapshot) 
   
def main():
    #connect to the db, and get the collections 
    client = MongoClient('localhost',27017)
    db = client.brofiler
    top_c = db.top
    netstat_c = db.netstat
    capstat_c = db.capstat

    #clean them on every run 
    top_c.remove()
    netstat_c.remove()
    capstat_c.remove()

    starttime = time.time()
    #broctl_refresh()
    file_init()

    test_config = system_config(
        '/usr/local/bro/etc/node.cfg',
        '/home/user/local.bro')
    test_device = bro_device('TEST', 'worker', '1.1.1.1', 'eth0')

    # test_config.modify_local_file('TEST_SCRIPT')
    # test_config.modify_node_config(test_device)

    # this collects a snapshot every x seconds
    for i in range(0, 100):

        top_snapshot = collect_top()
        # top_snapshot[0].print_all()
        add_to_db(top_snapshot, top_c)

        netstat_snapshot = collect_netstats() 
        # netstat_snapshot[0].print_all()
        add_to_db(netstat_snapshot, netstat_c) 

        capstat_snapshot = collect_capstats() 
        add_to_db(capstat_snapshot, capstat_c) 

        i += 1 
        time.sleep(3.0 - ((time.time() - starttime) % 3.0))

if __name__ == "__main__":
    main()
