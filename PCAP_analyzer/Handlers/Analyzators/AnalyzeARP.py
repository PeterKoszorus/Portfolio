# This module will have implementation for handling the analyze arp part of the assignment
from Classes.StreamClasses.ARPStream import Stream as st


class Analyze:

    def __init__(self, encap_data):
        self.all_encap_data = encap_data
        self.communications = self.collect_communication()

    # This method will collect all frames from one communication
    def collect_communication(self):
        communications = []
        create = True

        for data in self.all_encap_data:
            if data.frame_header.nested_protocol == "ARP (Address Resolution Protocol)":
                if communications:
                    for communication in communications:
                        if communication.smac == data.arp_header.smac and \
                                communication.sip == data.arp_header.sip and \
                                communication.dmac == data.arp_header.dmac and \
                                communication.dip == data.arp_header.dip and not communication.ended:
                            communication.append_communication(data)
                            create = False
                            break
                        elif communication.sip == data.arp_header.dip and \
                                communication.dip == data.arp_header.sip and \
                                communication.dmac == data.arp_header.smac and not communication.ended:
                            communication.append_communication(data)
                            communication.ended = True
                            create = False
                            break
                    if create:
                        new_communication = st(data.arp_header.sip, data.arp_header.dip, data.arp_header.smac,
                                               data.arp_header.dmac)
                        new_communication.append_communication(data)
                        communications.append(new_communication)
                    else:
                        create = True
                else:
                    new_communication = st(data.arp_header.sip, data.arp_header.dip, data.arp_header.smac,
                                           data.arp_header.dmac)
                    new_communication.append_communication(data)
                    communications.append(new_communication)

        return communications

    # This method prints out all each communication
    def print_arp(self):
        for i, data in enumerate(self.communications):
            data.print_communication(i)
