# This method will house one whole communication of type


class Stream:

    def __init__(self, s_address, d_address, s_physical, d_physical):
        self.smac = s_physical
        self.sip = s_address
        self.dmac = d_physical
        self.dip = d_address
        self.ended = False
        self.communication = []

    # This method will add frame to the communication list
    def append_communication(self, frame):
        self.communication.append(frame)

    # Method which prints out communications
    def print_communication(self, com_num):
        print("{}{}".format("-----COMMUNICATION-----", com_num))
        print("{}{}".format("Completed communication: ", self.ended))
        if len(self.communication) > 20:
            for data in self.communication[:10]:
                print("ARP HEADER")
                data.arp_header.print_arp()
                data.print_encapsulated_data()
            print("..................")
            for data in self.communication[-10:]:
                data.arp_header.print_arp()
                data.print_encapsulated_data()
        else:
            for data in self.communication:
                print("ARP HEADER")
                data.arp_header.print_arp()
                data.print_encapsulated_data()
