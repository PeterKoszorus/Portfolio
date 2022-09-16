# This module is housing the Segment Header class
import Handlers.JsonExtractor as je
from Utilities.HexTools import ToDec as td


class SegmentHeader:

    def __init__(self, raw_segment, seg_type):
        self.raw_segment = raw_segment
        self.seg_type = seg_type
        self.flag = None
        self.s_port = self.get_port("source")
        self.d_port = self.get_port("dest")

    # This method will return the source port of segment header
    def get_source_port(self):
        return str(td(self.raw_segment[:4]))

    # This method will return the destination port of segment header
    def get_destination_port(self):
        return str(td(self.raw_segment[4:8]))

    # This method will set the flag for the TCP
    def set_flag(self, flag):
        self.flag = flag

    # This method gets the source and destination and checks if are well known
    def get_port(self, arg):

        well_knowns = je.load_ports()

        if arg == "source":
            port = self.get_source_port()
        elif arg == "dest":
            port = self.get_destination_port()
        else:
            return None

        for well_known in well_knowns[self.seg_type]:
            if well_known == port:
                return port + " well known-" + well_knowns[self.seg_type][port]

        return port

    # This method will print all the data of SegmentHeader
    def print_seg_header(self):
        print("SEGMENT HEADER INFORMATION")
        print("{}{}".format("Segment type: ", self.seg_type))
        print("{}{}".format("Source port: ", self.s_port))
        print("{}{}".format("Destination port: ", self.d_port))
        if self.flag is not None:
            print("COMMUNICATION FLAGS")
            print(self.flag)


