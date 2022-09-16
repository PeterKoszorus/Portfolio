
class Stream:

    def __init__(self, sip, dip, sport, dport):
        self.sip = sip
        self.dip = dip
        self.sport = sport
        self.dport = dport
        self.communication = []

    # This method will add frame to the communication list
    def append_communication(self, frame):
        self.communication.append(frame)

    # Method which prints out communications
    def print_communication(self, com_num):
        print("{}{}".format("-----COMMUNICATION-----", com_num))

        for data in self.communication:
            data.print_encapsulated_data()
