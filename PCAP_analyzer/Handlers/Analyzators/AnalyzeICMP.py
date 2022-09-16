# This module filters out all the icmp frames and prints them out
import Handlers.JsonExtractor as je


# This function gets the type of icmp
def get_type(frame):
    icmp_type = je.load_icmp()

    for icmp in icmp_type:
        if icmp == frame.raw[frame.packet_header.ending_byte: frame.packet_header.ending_byte + 2]:
            return icmp_type[icmp]


class Analyze:

    def __init__(self, encap_data):
        self.all_encap_data = encap_data
        self.all_icmp = self.get_icmp()

    # This method returns the list of all frames with icmp
    def get_icmp(self):

        selected_data = []

        for data in self.all_encap_data:
            if data.packet_header is not None:
                if data.packet_header.protocol == "ICMP":
                    selected_data.append(data)

        if selected_data:
            return selected_data
        else:
            return None

    # This method prints out all of the icmp traffic from selected pcap
    def print_icmp(self):
        for data in self.all_icmp:
            print("{}{}".format("ICMP type: ", get_type(data)))
            data.print_encapsulated_data()
