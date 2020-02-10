import sys

from p4utils.utils.topology import Topology
from p4utils.utils.sswitch_API import SimpleSwitchAPI

class ReadCounter(object):
    def __init__(self):
        
        self.topo        = Topology(db="topology.db")
        self.controllers = {}
        self.init()

    def init(self):
        self.connect_to_switches()

    def connect_to_switches(self):
        for p4switch in self.topo.get_p4switches():
            thrift_port = self.topo.get_thrift_port(p4switch)
            self.controllers[p4switch] = SimpleSwitchAPI(thrift_port)

    def read_indirect_counters(self):

        for sw_name, controller in self.controllers.items():
            for i in range(10):
                self.controllers[sw_name].counter_read("port_counter", i)

    def read_direct_counters(self):

        for sw_name, controller in self.controllers.items():
            num_table_entries = self.controllers[sw_name].table_num_entries('ipv4_lpm')
            for i in range(int(num_table_entries)):
                self.controllers[sw_name].counter_read("direct_port_counter", i)

def main():
    counter_type = sys.argv[1]
    if counter_type == 'indirect':
        read_counter = ReadCounter().read_indirect_counters()
    elif counter_type == 'direct':
        read_counter = ReadCounter().read_direct_counters()
    else:
        raise ValueError('Unknown counter type: {0}'.format(counter_type))

if __name__ == '__main__':
    main()