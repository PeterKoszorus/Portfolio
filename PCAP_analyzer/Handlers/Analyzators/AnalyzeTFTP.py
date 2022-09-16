# This method will be responsible for analyzing the tftp communication
from Classes.StreamClasses.TFTPStream import Stream as st


class Analyze:

    def __init__(self, encap_data):
        self.all_encap_data = encap_data
        self.communications = self.filter_communication()

    # This method will filter each communication one by one
    def filter_communication(self):
        communications = []

        for i, data in enumerate(self.all_encap_data):
            if data.segment_header is not None:
                if "tftp" in data.segment_header.s_port or "tftp" in data.segment_header.d_port:
                    new_communication = st(self.all_encap_data[i + 1].packet_header.s_address,
                                           self.all_encap_data[i + 1].packet_header.d_address,
                                           self.all_encap_data[i + 1].segment_header.s_port,
                                           self.all_encap_data[i + 1].segment_header.d_port)
                    new_communication.append_communication(data)
                    communications.append(new_communication)
        if communications:
            for communication in communications:
                for data in self.all_encap_data:
                    if data.packet_header is not None and data.segment_header is not None:
                        # condition to check if the communication is from the same group
                        if ((data.packet_header.s_address == communication.sip and
                             data.packet_header.d_address == communication.dip) or
                            (data.packet_header.s_address == communication.dip and
                             data.packet_header.d_address == communication.sip)) and \
                                ((data.segment_header.s_port == communication.sport and
                                  data.segment_header.d_port == communication.dport) or
                                 (data.segment_header.s_port == communication.dport and
                                  data.segment_header.d_port == communication.sport)):

                            communication.append_communication(data)
            return communications
        else:
            return None

    # This method prints out every tftp communications
    def print_tftp(self):
        for i, communication in enumerate(self.communications):
            communication.print_communication(i)
