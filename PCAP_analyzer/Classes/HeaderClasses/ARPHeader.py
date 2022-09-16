# This module is housing the ARPHeader class
from Utilities.HexTools import ToDec as td


class ARPHeader:

    def __init__(self, raw):
        self.raw_arp = raw
        self.reply = self.get_opcode()
        self.smac = self.get_sender_mac()
        self.sip = self.get_sender_ip()
        self.dmac = self.get_destination_mac()
        self.dip = self.get_destination_ip()

    # This method returns true if its reply and false if it is request
    def get_opcode(self):
        if self.raw_arp[15:16] == "1":
            return False
        elif self.raw_arp[15:16] == "2":
            return True

    # This method returns the source mac address
    def get_sender_mac(self):
        return self.raw_arp[16:28]

    # This method returns the source ip address
    def get_sender_ip(self):
        first_byte = td(self.raw_arp[28:30])
        second_byte = td(self.raw_arp[30:32])
        third_byte = td(self.raw_arp[32:34])
        fourth_byte = td(self.raw_arp[34:36])
        return str(first_byte) + "." + str(second_byte) + "." + str(third_byte) + "." + str(fourth_byte)

    # This method returns the destination mac address
    def get_destination_mac(self):
        return self.raw_arp[36:48]

    # This method returns the destination ip address
    def get_destination_ip(self):
        first_byte = td(self.raw_arp[48:50])
        second_byte = td(self.raw_arp[50:52])
        third_byte = td(self.raw_arp[52:54])
        fourth_byte = td(self.raw_arp[54:])
        return str(first_byte) + "." + str(second_byte) + "." + str(third_byte) + "." + str(fourth_byte)

    # This method prints out all of the arp header parameters
    def print_arp(self):
        if self.reply:
            print("reply")
        else:
            print("request")
        print("{}{}".format("Sender MAC address: ", self.smac))
        print("{}{}".format("Sender IP address: ", self.sip))
        print("{}{}".format("Destination MAC address: ", self.dmac))
        print("{}{}".format("Destination IP address: ", self.dip))
