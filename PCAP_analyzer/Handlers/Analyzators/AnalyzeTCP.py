# This module will have implementation for handling the analyze tcp part of the assignment
from Classes.StreamClasses.TCPStream import Stream as st


class Analyze:

    def __init__(self, encap_data, communication):
        self.all_encap_data = encap_data
        self.communication = communication
        self.selected_data = self.select_data()
        self.one_stream = self.collect_communication()

    # This method filters out from all_encap_data only the ones which are required for further processing
    def select_data(self):
        selected_data = []
        for encap_data in self.all_encap_data:
            if encap_data.segment_header is not None:
                if self.communication in encap_data.segment_header.s_port or \
                        self.communication in encap_data.segment_header.d_port:
                    selected_data.append(encap_data)

        if selected_data:
            return selected_data
        else:
            return None

    # This method will collect all frames from one communication
    def collect_communication(self):

        if self.selected_data is not None:
            temp_list = self.select_data().copy()
        else:
            return None
        communications = []
        if temp_list[0].segment_header.seg_type == "TCP":
            while temp_list:

                new_communication = st(temp_list[0].packet_header.s_address, temp_list[0].packet_header.d_address,
                                       temp_list[0].segment_header.s_port, temp_list[0].segment_header.d_port)

                communications.append(new_communication)

                for i, data in enumerate(temp_list):

                    # condition to check if the communication is from the same group
                    if ((data.packet_header.s_address == new_communication.s_address and
                         data.packet_header.d_address == new_communication.d_address) or
                        (data.packet_header.s_address == new_communication.d_address and
                         data.packet_header.d_address == new_communication.s_address)) and \
                            ((data.segment_header.s_port == new_communication.s_port and
                              data.segment_header.d_port == new_communication.d_port) or
                             (data.segment_header.s_port == new_communication.d_port and
                              data.segment_header.d_port == new_communication.s_port)):
                        new_communication.append_communication(data)

                # After storing one whole communication this deletes the ones which were stored
                for data in new_communication.list_of_communication:
                    temp_list.remove(data)

            return communications
        else:
            return None

    # This method will get the flags for each communication chain
    def get_flags(self):
        if self.one_stream is not None:
            for communication in self.one_stream:
                communication.get_the_flag()
        else:
            return None

    # This method gets checks if the communication was successfully opened and ended and also load the flags
    def check_completnes(self):

        if self.one_stream is not None:
            self.get_flags()

            for communication in self.one_stream:
                communication.complete_start = communication.check_complete_start()
                communication.complete_end = communication.check_complete_end()
        else:
            return None

    # This method will print each communication of TCP
    def print_analyze_tcp(self):

        if self.one_stream is not None:

            self.check_completnes()

            for i, data in enumerate(self.one_stream):
                # Prints out the first whole communication from the list of communications
                if data.complete_end and data.complete_start:
                    print("-----completed communication-----")
                    data.print_communication(i)
                    break

            for i, data in enumerate(self.one_stream):
                # Prints out the first incomplete communication from the list of communications
                if data.complete_start and not data.complete_end:
                    print("-----Uncompleted communication-----")
                    data.print_communication(i)
                    return True
        else:
            return None
