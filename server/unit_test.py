import yaml

def parse_unit(unit_test_file):
    unit_tests = []

    with open(unit_test_file,'r') as unit_file:
        cfg = yaml.load(unit_file)

    for section in cfg:
        source = cfg[section]['source']
        pcap = cfg[section]['pcap']
        count = cfg[section]['count']
        test = unit_test(source,pcap,count)
        unit_tests.append(test)

    return unit_tests

class unit_test(object):

    def __init__(self,source,pcap_path,count):
        self.source = source
        self.pcap_path = pcap_path
        self.count = count

    def load_pcaps():
        print("TODO")
        #send pcap files to traffic generator

    def start_test():
        print("TODO")
        #send message to traffic generator to start transmitting
