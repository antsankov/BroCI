#This is where we parse the unit test file and generate an array of test objects for us to run. 

import yaml
import os

def run_tests():
    tests = parse_unit('./REPO/unittest.yaml') 
    for test in tests:
        test.start()

def parse_unit(unit_test_file):
    unit_tests = []

    with open(unit_test_file,'r') as unit_file:
        cfg = yaml.load(unit_file)

    for section in cfg:
        print(section)
        source = cfg[section]['source']
        pcap  = "./REPO/{}".format(cfg[section]['pcap']) 
        count = cfg[section]['count']
        inteface = cfg[section]['interface']
        test = unit_test(source,pcap,count,inteface)
        unit_tests.append(test)

    return unit_tests

class unit_test(object):

    def __init__(self,source,pcap_path,count,interface):
        self.source = source
        self.pcap_path = pcap_path
        self.count = count
        self.interface = interface

    def load_pcaps(self):
        print("TODO")
        #send pcap files to traffic generator

    def start(self): 
        command_string = "tcpreplay --topspeed --loop={count} -i {interface} {pcap} &".format(count = self.count, interface = self.interface, pcap = self.pcap_path)
        print(command_string)
        os.system(command_string)
        print("DONE")
