# This method will house one whole communication of type
from Utilities.HexTools import ToDec as td


class Stream:

    def __init__(self, ip_1, ip_2, port_1, port_2):
        self.s_address = ip_1
        self.d_address = ip_2
        self.s_port = port_1
        self.d_port = port_2
        self.list_of_communication = []
        self.complete_start = False
        self.complete_end = False

    # This method will add frame to the communication list
    def append_communication(self, frame):
        self.list_of_communication.append(frame)

    # This method gets all the flags for each communication
    def get_the_flag(self):

        for data in self.list_of_communication:
            raw_flag = data.segment_header.raw_segment[25:28]

            flag_in_dec = int(td(raw_flag))

            if flag_in_dec == 1:
                data.segment_header.set_flag("FIN")
            elif flag_in_dec == 2:
                data.segment_header.set_flag("SYN")
            elif flag_in_dec == 4:
                data.segment_header.set_flag("RST")
            elif flag_in_dec == 8:
                data.segment_header.set_flag("PSH")
            elif flag_in_dec == 16:
                data.segment_header.set_flag("ACK")
            elif flag_in_dec == 17:
                data.segment_header.set_flag("FIN, ACK")
            elif flag_in_dec == 18:
                data.segment_header.set_flag("SYN, ACK")
            elif flag_in_dec == 24:
                data.segment_header.set_flag("PSH, ACK")
            else:
                data.segment_header.set_flag(flag_in_dec)

    # This method checks if communication is complete or not
    def check_complete_end(self):

        # This condition is for RST flag coming from client/server side
        if (self.list_of_communication[-1].segment_header.flag == "RST" and
                self.list_of_communication[-1].segment_header.s_port == self.d_port and
                self.list_of_communication[-1].segment_header.d_port == self.s_port) or \
                (self.list_of_communication[-1].segment_header.flag == "RST" and
                 self.list_of_communication[-1].segment_header.s_port == self.s_port and
                 self.list_of_communication[-1].segment_header.d_port == self.d_port):
            return True

        # This condition is for three way handshake at the end
        elif self.list_of_communication[-3].segment_header.flag == "FIN":

            if self.list_of_communication[-2].segment_header.flag == "FIN, ACK":

                if self.list_of_communication[-1].segment_header.flag == "ACK":
                    return True
                else:
                    return False
            else:
                return False

        # This conditions is for four way handshake
        elif self.list_of_communication[-4].segment_header.flag == "FIN":

            if self.list_of_communication[-3].segment_header.flag == "ACK":

                if self.list_of_communication[-2].segment_header.flag == "FIN":

                    if self.list_of_communication[-1].segment_header.flag == "ACK":

                        return True
                    else:
                        return False
                else:
                    return False
        elif self.list_of_communication[-4].segment_header.flag == "FIN, ACK":

            if self.list_of_communication[-3].segment_header.flag == "ACK":

                if self.list_of_communication[-2].segment_header.flag == "FIN, ACK":

                    if self.list_of_communication[-1].segment_header.flag == "ACK":
                        return True
                else:
                    return False
            else:
                return False
        else:
            return False

    # This method checks if at the start of communication the three-way handshake was alright
    def check_complete_start(self):

        if self.list_of_communication[0].segment_header.flag == "SYN" and \
                self.list_of_communication[0].segment_header.s_port == self.s_port and \
                self.list_of_communication[0].segment_header.d_port == self.d_port:

            if self.list_of_communication[1].segment_header.flag == "SYN, ACK" and \
                    self.list_of_communication[1].segment_header.s_port == self.d_port and \
                    self.list_of_communication[1].segment_header.d_port == self.s_port:

                if self.list_of_communication[2].segment_header.flag == "ACK" and \
                        self.list_of_communication[2].segment_header.s_port == self.s_port and \
                        self.list_of_communication[2].segment_header.d_port == self.d_port:
                    return True
                else:
                    return False
            else:
                return False

        else:
            return False

    # Method which prints out communications
    def print_communication(self, com_num):
        print("{}{}".format("-----COMMUNICATION-----", com_num))
        if len(self.list_of_communication) > 20:
            for data in self.list_of_communication[:10]:
                data.print_encapsulated_data()
            for data in self.list_of_communication[-10:]:
                data.print_encapsulated_data()
        else:
            for data in self.list_of_communication:
                data.print_encapsulated_data()
