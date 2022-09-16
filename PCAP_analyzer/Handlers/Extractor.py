# Extractor here will be the logic for taking the data from .pcap and will send it to the frame class
import os
import scapy.all as scapy
from Classes.EncapsulatedData import EncapsulatedData as ed


# Have to rework the logic behind opening pcap, maybe secure this class as by singleton design pattern
# trace 20 - 25 su RAW


class FrameLoader:
    # Later i ll get the pcap name as argument as well
    def __init__(self, dirname, pcap_name):
        self.dirname = dirname
        self.pcap = self.set_pcap(pcap_name)

    # Method which gets the the path of the directory where the pcap are located
    def set_pcap(self, pcap_name):
        try:
            return scapy.rdpcap(os.path.join(self.dirname, "Resources\\vzorky_pcap_na_analyzu\\" + pcap_name))
        except FileNotFoundError:
            print("{}{}".format("Didnt find file named: ", pcap_name))
            return None

    # Loads the pcap file and creates objects for each Frame
    # Return: list of FrameObjects
    def load_raw(self):
        encap_data = []
        i = 1
        for pkt in self.pcap:
            encap_data.append(ed(scapy.raw(pkt).hex(), i, len(pkt)))
            i += 1

        return encap_data
