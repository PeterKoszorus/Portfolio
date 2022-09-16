# This module will house class for the implementation of IpHeader
import Handlers.JsonExtractor as je
from Utilities.HexTools import ToDec as td


class IpHeader:

    def __init__(self, raw_packet, version, ihl):
        self.raw_packet = raw_packet
        self.version = version
        self.ending_byte = 28 + ihl
        self.ihl = int((ihl / 2))
        self.protocol = self.get_protocol()
        self.s_address = self.get_source_address()
        self.d_address = self.get_destination_address()

    # This method will return the protocol of IpHeader
    def get_protocol(self):
        protocols = je.load_ip_protocols()
        for protocol in protocols:
            if protocol == self.raw_packet[18:20]:
                return protocols[protocol]

    # This method returns the source address of frame in string 192.168.1.1 format
    def get_source_address(self):
        first_byte = td(self.raw_packet[24:26])
        second_byte = td(self.raw_packet[26:28])
        third_byte = td(self.raw_packet[28:30])
        fourth_byte = td(self.raw_packet[30:32])

        return str(first_byte) + "." + str(second_byte) + "." + str(third_byte) + "." + str(fourth_byte)

    # This method returns the source address of frame in string 192.168.1.1 format
    def get_destination_address(self):
        first_byte = td(self.raw_packet[32:34])
        second_byte = td(self.raw_packet[34:36])
        third_byte = td(self.raw_packet[36:38])
        fourth_byte = td(self.raw_packet[38:40])

        return str(first_byte) + "." + str(second_byte) + "." + str(third_byte) + "." + str(fourth_byte)

    # This method helps with converting the data to pandas dataframe in Handlers.IPstatistics
    def to_dict(self):
        return {"version": self.version, "ihl": self.ihl, "protocol": self.protocol,
                "source_address": self.s_address,
                "destination_address": self.d_address}

    # This method prints out all the useful data
    def print_packet_header(self):
        print("PACKET HEADER INFORMATION")
        print("{}{}".format("IP header version: ", self.version))
        print("{}{}{}".format("IPv4 header length: ", self.ihl, " B"))
        print("{}{}".format("Protocol: ", self.protocol))
        print("{}{}".format("Source IP address: ", self.s_address))
        print("{}{}".format("Destination IP address: ", self.d_address))
